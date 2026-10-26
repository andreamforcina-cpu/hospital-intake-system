import random
import unittest
from doctor_tree import DoctorNode, DoctorTree
from emergency_queue import Patient, MinHeap


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.tree = DoctorTree()
        self.tree.root = DoctorNode('Dr. Croft')
        for parent, name, side in [
            ('Dr. Croft', 'Dr. Goldsmith', 'right'),
            ('Dr. Croft', 'Dr. Phan', 'left'),
            ('Dr. Phan', 'Dr. Carson', 'right'),
            ('Dr. Phan', 'Dr. Morgan', 'left')]:
            self.assertTrue(self.tree.insert(parent, name, side))

    def test_traversals(self):
        self.assertEqual(self.tree.preorder(self.tree.root),
                         ['Dr. Croft', 'Dr. Phan', 'Dr. Morgan', 'Dr. Carson', 'Dr. Goldsmith'])
        self.assertEqual(self.tree.inorder(self.tree.root),
                         ['Dr. Morgan', 'Dr. Phan', 'Dr. Carson', 'Dr. Croft', 'Dr. Goldsmith'])
        self.assertEqual(self.tree.postorder(self.tree.root),
                         ['Dr. Morgan', 'Dr. Carson', 'Dr. Phan', 'Dr. Goldsmith', 'Dr. Croft'])

    def test_invalid_insert_preserves_tree(self):
        before = self.tree.preorder(self.tree.root)
        for args in [('Missing', 'New', 'left'), ('Dr. Croft', 'New', 'up'),
                     ('Dr. Croft', 'New', 'left'), ('Dr. Morgan', 'Dr. Croft', 'left')]:
            self.assertFalse(self.tree.insert(*args))
        self.assertEqual(self.tree.preorder(self.tree.root), before)

    def test_empty_and_single(self):
        for traversal in (self.tree.preorder, self.tree.inorder, self.tree.postorder):
            self.assertEqual(traversal(None), [])
            self.assertEqual(traversal(DoctorNode('Solo')), ['Solo'])
        self.assertFalse(DoctorTree().insert('Missing', 'New', 'left'))


class HeapTests(unittest.TestCase):
    def assert_heap(self, heap):
        for index in range(1, len(heap.data)):
            self.assertLessEqual(heap.data[(index - 1) // 2].urgency, heap.data[index].urgency)

    def test_assignment_example_and_peek(self):
        heap = MinHeap()
        patients = [Patient('Jordan', 3), Patient('Taylor', 1), Patient('Avery', 5)]
        for patient in patients:
            heap.insert(patient)
        self.assertIs(heap.peek(), patients[1])
        self.assertEqual(len(heap.data), 3)
        self.assertEqual([heap.remove_min().name for _ in patients], ['Taylor', 'Jordan', 'Avery'])

    def test_empty_and_single(self):
        heap = MinHeap()
        for operation in (heap.peek, heap.remove_min):
            with self.assertRaises(IndexError):
                operation()
        patient = Patient('Solo', 10)
        heap.insert(patient)
        self.assertIs(heap.remove_min(), patient)
        self.assertEqual(heap.data, [])

    def test_randomized_interleaved_operations(self):
        rng = random.Random(7)
        heap = MinHeap()
        waiting = []
        for index in range(500):
            if not waiting or rng.random() < 0.65:
                patient = Patient(str(index), rng.randint(1, 10))
                waiting.append(patient)
                heap.insert(patient)
            else:
                expected = min(p.urgency for p in waiting)
                served = heap.remove_min()
                self.assertEqual(served.urgency, expected)
                waiting.remove(served)
            self.assert_heap(heap)
        expected = sorted(p.urgency for p in waiting)
        self.assertEqual([heap.remove_min().urgency for _ in waiting], expected)

    def test_validation(self):
        for urgency in (0, 11, True, 2.5, '2'):
            with self.assertRaises(ValueError):
                Patient('Name', urgency)
        with self.assertRaises(ValueError):
            Patient('', 1)
        with self.assertRaises(TypeError):
            MinHeap().insert('not a patient')


if __name__ == '__main__':
    unittest.main()
