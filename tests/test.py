import unittest
from PIL import Image
from pathlib import Path

# Import the predict function from main.py
from app.main import predict


class TestPredictFunction(unittest.TestCase):
    def setUp(self):
        """
        Set up any necessary data for the tests.
        """
        # Load the test image from the correct path
        test_image_path = Path(__file__).resolve().parent / "test_image.png"
        self.test_image = Image.open(test_image_path).convert("L")
        self.test_image = self.test_image.resize((28, 28))

    def test_predict_output(self):
        """
        Test if the predict function returns an integer (digit).
        """
        result = predict(self.test_image).item()
        self.assertIsInstance(result, int, "The predict function should return an integer.")

    def test_predict_with_realistic_data(self):
        """
        Test if the predict function returns a reasonable digit for a basic image.
        """
        result = predict(self.test_image)
        self.assertIn(result, range(10), "The prediction should be a digit between 0 and 9.")


if __name__ == '__main__':
    unittest.main()
