import unittest
import numpy as np
from typing import List, Tuple
from .transform_constraints import transform_constraints
from .setup_tableau import setup_tableau
from .pivot import select_entering_variable, select_leaving_variable, pivot
from .solution_extraction import extract_solution
import logging

# Set up logging
logger = logging.getLogger(__name__)

class TestSimplex(unittest.TestCase):
    
    def test_transform_constraints(self):
        # Test case 1: No '>=' constraints
        A1 = np.array([[1, 2], [3, 4]])
        b1 = np.array([5, 6])
        senses1 = ['<=', '<=']
        A1_trans, b1_trans = transform_constraints(A1, b1, senses1)
        self.assertTrue(np.array_equal(A1_trans, A1))
        self.assertTrue(np.array_equal(b1_trans, b1))
        
        # Test case 2: One '>=' constraint
        A2 = np.array([[1, 2], [3, 4]])
        b2 = np.array([5, 6])
        senses2 = ['<=', '>=']
        A2_trans, b2_trans = transform_constraints(A2, b2, senses2)
        self.assertTrue(np.array_equal(A2_trans, np.array([[1, 2], [-3, -4]])))
        self.assertTrue(np.array_equal(b2_trans, np.array([5, -6])))
        
        # Test case 3: All '>=' constraints
        A3 = np.array([[1, 2], [3, 4]])
        b3 = np.array([5, 6])
        senses3 = ['>=', '>=']
        A3_trans, b3_trans = transform_constraints(A3, b3, senses3)
        self.assertTrue(np.array_equal(A3_trans, np.array([[-1, -2], [-3, -4]])))
        self.assertTrue(np.array_equal(b3_trans, np.array([-5, -6])))
    
    def test_setup_tableau(self):
        # Test case 1: Maximization problem with all '<=' constraints
        c1 = np.array([3, 5])
        A1 = np.array([[1, 2], [3, 4]])
        b1 = np.array([5, 6])
        senses1 = ['<=', '<=']
        tableau1 = setup_tableau(c1, A1, b1, senses1)
        expected_tableau1 = np.array([[3, 5, 0, 0, 0],
                                        [1, 2, 1, 0, 5],
                                        [3, 4, 0, 1, 6]])
        self.assertTrue(np.allclose(tableau1, expected_tableau1))
        
        # Test case 2: Minimization problem with mixed constraints
        c2 = np.array([2, 3])
        A2 = np.array([[1, 1], [1, -1]])
        b2 = np.array([10, 5])
        senses2 = ['>=', '=']
        tableau2 = setup_tableau(c2, A2, b2, senses2, prob_type='min')
        expected_tableau2 = np.array([[-2, -3, 0, 0, 0],
                                        [1, 1, -1, 1, 10],
                                        [1, -1, 0, 1, 5]])
        self.assertTrue(np.allclose(tableau2, expected_tableau2))
    
    def test_select_entering_variable(self):
        # Test case 1
        tableau1 = np.array([[ -3, -5, 0, 0, 0],
                             [ 1, 2, 1, 0, 5],
                             [ 3, 4, 0, 1, 6]])
        entering_col1 = select_entering_variable(tableau1)
        self.assertEqual(entering_col1, 1)
        
        # Test case 2
        tableau2 = np.array([[ 0, 0, 1, -2, 0],
                             [ 1, 0, 0, 1, 3],
                             [ 0, 1, 0, -1, 2]])
        entering_col2 = select_entering_variable(tableau2)
        self.assertEqual(entering_col2, 3)
    
    def test_calculate_ratios(self):
        # Test case 1
        tableau1 = np.array([[ -3, -5, 0, 0, 0],
                             [ 1, 2, 1, 0, 5],
                             [ 3, 4, 0, 1, 6]])
        ratios1 = calculate_ratios(tableau1, 1)
        expected_ratios1 = np.array([2.5, 1.5])
        self.assertTrue(np.allclose(ratios1, expected_ratios1))
        
        # Test case 2
        tableau2 = np.array([[ 0, 0, 1, -2, 0],
                             [ 1, 0, 0, 1, 3],
                             [ 0, 1, 0, -1, 2]])
        ratios2 = calculate_ratios(tableau2, 3)
        expected_ratios2 = np.array([3.0, -2.0])
        self.assertTrue(np.allclose(ratios2, expected_ratios2))
    
    def test_select_leaving_variable(self):
        # Test case 1
        tableau1 = np.array([[ -3, -5, 0, 0, 0],
                             [ 1, 2, 1, 0, 5],
                             [ 3, 4, 0, 1, 6]])
        leaving_row1 = select_leaving_variable(tableau1, 1)
        self.assertEqual(leaving_row1, 2)
        
        # Test case 2
        tableau2 = np.array([[ 0, 0, 1, -2, 0],
                             [ 1, 0, 0, 1, 3],
                             [ 0, 1, 0, -1, 2]])
        leaving_row2 = select_leaving_variable(tableau2, 3)
        self.assertEqual(leaving_row2, None)
    
    def test_pivot(self):
        # Test case 1
        tableau1 = np.array([[ -3, -5, 0, 0, 0],
                             [ 1, 2, 1, 0, 5],
                             [ 3, 4, 0, 1, 6]])
        pivoted_tableau1 = pivot(tableau1.copy(), 1, 2)
        expected_tableau1 = np.array([[1.5, 0, 0, 1.25, 7.5],
                                     [-0.5, 0, 1, -0.5, 2.0],
                                     [0.75, 1, 0, 0.25, 1.5]])
        self.assertTrue(np.allclose(pivoted_tableau1, expected_tableau1))
    
    def test_extract_solution(self):
        # Test case 1: Maximization problem
        tableau1 = np.array([[0, 0, 1.25, 0.75, 31.25],
                             [1, 0, 0.25, -0.25, 1.25],
                             [0, 1, -0.75, 0.25, 2.75]])
        x1, z1 = extract_solution(tableau1, 2, 2, prob_type='max')
        expected_x1 = np.array([1.25, 2.75])
        expected_z1 = 31.25
        self.assertTrue(np.allclose(x1, expected_x1))
        self.assertAlmostEqual(z1, expected_z1)
        
        # Test case 2: Minimization problem
        tableau2 = np.array([[0, 0, -1.25, -0.75, -31.25],
                             [1, 0, 0.25, -0.25, 1.25],
                             [0, 1, -0.75, 0.25, 2.75]])
        x2, z2 = extract_solution(tableau2, 2, 2, prob_type='min')
        expected_x2 = np.array([1.25, 2.75])
        expected_z2 = 31.25
        self.assertTrue(np.allclose(x2, expected_x2))
        self.assertAlmostEqual(z2, expected_z2)

if __name__ == '__main__':
    unittest.main()
