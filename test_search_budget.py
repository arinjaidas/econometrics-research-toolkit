import unittest
import numpy as np
import pandas as pd
from toolkit import compare_models


class SearchBudgetTests(unittest.TestCase):
    def test_large_search_rejected_before_enumeration(self):
        rng = np.random.default_rng(1)
        controls = [f'control_{i}' for i in range(36)]
        frame = pd.DataFrame(rng.normal(size=(100, 38)), columns=['y', 'base'] + controls)
        with self.assertRaisesRegex(ValueError, 'max_models'):
            compare_models(frame, 'y', ['base'], controls, max_controls=18, max_models=256)


if __name__ == '__main__': unittest.main()
