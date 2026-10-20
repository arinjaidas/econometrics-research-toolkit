import unittest
import numpy as np
from toolkit import synthetic_data,compare_models


class ResearchToolkitChecks(unittest.TestCase):
    def test_comparable_samples_and_known_association(self):
        data,table,fits,skipped=compare_models(synthetic_data(),'life_expectancy',['numeracy'],['coast_distance','climate','missions','population'])
        self.assertEqual(table.n.nunique(),1)
        self.assertEqual(int(table.n.iloc[0]),len(data))
        self.assertEqual(len(table),15)
        self.assertTrue(np.isfinite(table[['aic','bic','adjusted_r_squared']]).all().all())
        self.assertTrue(all(3<fit.params['numeracy']<5 for _,fit in fits.values()))

    def test_rank_deficient_controls_are_reported(self):
        frame=synthetic_data();frame['duplicate']=frame.numeracy
        _,table,_,skipped=compare_models(frame,'life_expectancy',['numeracy'],['duplicate'])
        self.assertEqual(len(table),1);self.assertEqual(len(skipped),1)

    def test_search_limit_prevents_accidental_explosion(self):
        with self.assertRaises(ValueError):
            compare_models(synthetic_data(),'life_expectancy',['numeracy'],['coast_distance','climate','missions','population'],max_models=2)

    def test_outcome_cannot_be_predictor(self):
        with self.assertRaises(ValueError):compare_models(synthetic_data(),'life_expectancy',['life_expectancy'],[])


if __name__=='__main__':unittest.main()
