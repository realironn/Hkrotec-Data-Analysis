"""Exercise additional-data imports, time separation and saved-model prediction."""
import ast
import json
from pathlib import Path
import tempfile
import unittest

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
notebook = json.loads((ROOT / '한국로텍_데이터분석.ipynb').read_text(encoding='utf-8'))
cell = next(c for c in notebook['cells'] if 'rotec-additional-data' in c.get('metadata', {}).get('tags', []))
tree = ast.parse(''.join(cell['source']))
definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               or (isinstance(node, ast.Assign) and all(isinstance(t, ast.Name)
                   and t.id.startswith('ADDITIONAL_') for t in node.targets))]
scope = {}
exec(compile(ast.Module(body=definitions, type_ignores=[]), '<additional-data>', 'exec'), scope)


class AdditionalDataTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.out = self.root / 'result'
        dates = pd.date_range('2020-01-01', periods=80)
        self.history = pd.DataFrame({'date': dates, 'total_reviewed': 100,
                                     'pinhole_pit_count': 2 + np.arange(80) % 5})
        features = scope['ADDITIONAL_FEATURES']
        self.x = pd.DataFrame({c: 1 + np.arange(80) * 0.01 + i
                               for i, c in enumerate(features)}, index=dates)
        self.inbox = scope['prepare_additional_folders'](self.root)
        self.last = dates.max()

    def rows(self, count=2, inspected=True, start=1):
        dates = [self.last + pd.Timedelta(days=i) for i in range(start, start + count)]
        return pd.DataFrame({
            '날짜': [str(d.date()) for d in dates], '검사수량': 100 if inspected else '',
            '핀홀피트건수': 4 if inspected else '', '설정전류밀도_A_dm2': 120,
            '전압_V': 6, '온도_C': 40, '처리시간_초': 120,
        })

    def write(self, frame, name='new.csv'):
        path = self.inbox / name
        if path.suffix == '.xlsx':
            frame.to_excel(path, index=False)
        else:
            frame.to_csv(path, index=False, encoding='utf-8-sig')
        return path

    def run_analysis(self):
        return scope['analyze_additional_data'](self.root, self.out, self.history, self.x)

    def test_empty_inbox_creates_blank_templates_without_training(self):
        result = self.run_analysis()
        self.assertEqual(result['info']['status'], 'no_input')
        self.assertTrue((self.root / '추가자료/양식/추가자료_입력양식.xlsx').is_file())
        template = pd.read_csv(self.root / '추가자료/양식/추가자료_입력양식.csv')
        self.assertEqual(len(template), 0)
        self.assertEqual(list(template), list(scope['ADDITIONAL_COLUMNS']))
        self.assertFalse((self.out / '추가자료분석/핀홀피트_예측모델.joblib').exists())

    def test_labeled_and_unlabeled_files_refit_and_predict_without_time_leakage(self):
        self.write(self.rows(4))
        pending = self.rows(2, inspected=False, start=5)
        self.write(pending, 'future.xlsx')
        original = self.history.copy(deep=True)
        result = self.run_analysis()
        info = result['info']
        self.assertEqual(info['status'], 'passed')
        self.assertEqual(info['training_rows'], 84)
        self.assertEqual(info['new_labeled_rows'], 4)
        self.assertEqual(info['prediction_only_rows'], 2)
        self.assertEqual(info['training_end'], str((self.last + pd.Timedelta(days=4)).date()))
        self.assertLess(info['evaluation_training_end'], info['evaluation_test_start'])
        pd.testing.assert_frame_equal(original, self.history)
        saved = joblib.load(self.out / '추가자료분석/핀홀피트_예측모델.joblib')
        predicted = pd.read_csv(self.out / '추가자료분석/미검사자료_예측결과.csv')
        self.assertEqual(len(predicted), 2)
        self.assertTrue(np.isfinite(predicted.iloc[:, 1]).all())
        inputs = pending.rename(columns=scope['ADDITIONAL_COLUMNS']).reindex(columns=scope['ADDITIONAL_FEATURES'])
        expected = np.clip(saved['model'].predict(inputs), 0, None)
        np.testing.assert_allclose(predicted.iloc[:, 1], expected)
        cv = pd.read_csv(self.out / '추가자료분석/시간순_모델비교.csv')
        chosen = cv.groupby('방법')['평균 예측 오차(%p)'].mean().sort_values().index[0]
        self.assertEqual(info['selected_model'], chosen)
        monthly = pd.read_csv(self.out / '추가자료분석/월별_검사집계.csv')
        self.assertEqual(monthly['검사수량'].sum(), 8400)
        self.assertEqual(monthly['핀홀피트건수'].sum(), self.history['pinhole_pit_count'].sum() + 16)

    def test_unlabeled_input_predicts_without_claiming_new_training_labels(self):
        self.write(self.rows(inspected=False))
        info = self.run_analysis()['info']
        self.assertEqual(info['training_rows'], 80)
        self.assertEqual(info['new_labeled_rows'], 0)
        self.assertEqual(info['prediction_only_rows'], 2)

    def test_duplicate_dates_across_files_are_rejected(self):
        self.write(self.rows())
        self.write(self.rows(), 'duplicate.xlsx')
        with self.assertRaisesRegex(ValueError, '같은 날짜'):
            self.run_analysis()
        status = json.loads((self.out / '추가자료분석/실행정보.json').read_text())
        self.assertEqual(status['status'], 'failed')
        self.assertFalse((self.out / '추가자료분석/핀홀피트_예측모델.joblib').exists())

    def test_missing_column_identifies_file(self):
        self.write(self.rows().drop(columns='전압_V'))
        with self.assertRaisesRegex(ValueError, 'new.csv.*없는 열: 전압_V'):
            self.run_analysis()

    def test_replacing_historical_dates_is_rejected(self):
        frame = self.rows()
        frame.loc[0, '날짜'] = str(self.last.date())
        self.write(frame)
        with self.assertRaisesRegex(ValueError, '기존 검사자료의 마지막 날짜'):
            self.run_analysis()

    def test_partial_inspection_and_invalid_measurements_are_rejected(self):
        for column, value, message in [('검사수량', '', '함께 입력'),
                                       ('핀홀피트건수', -1, '0 이상'),
                                       ('온도_C', '문자', '숫자'),
                                       ('전압_V', 0.05, '0.1V 이하')]:
            with self.subTest(column=column):
                frame = self.rows().astype(object)
                frame.loc[0, column] = value
                self.write(frame)
                with self.assertRaisesRegex(ValueError, message):
                    self.run_analysis()

    def test_prediction_dates_cannot_precede_latest_training_label(self):
        self.write(self.rows(count=1, inspected=False, start=1))
        self.write(self.rows(count=1, inspected=True, start=2), 'later.csv')
        with self.assertRaisesRegex(ValueError, '마지막 학습일'):
            self.run_analysis()


if __name__ == '__main__':
    unittest.main()
