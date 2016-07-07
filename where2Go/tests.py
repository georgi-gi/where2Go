import unittest
import googlish
from landmark import Landmark
from db_and_forecast import sort_landmarks


class TestSorting(unittest.TestCase):
    def setUp(self):
        self.sample_response = {
            'routes': [
                {
                    'legs': [
                        {
                            'steps': [
                                {
                                    'html_instructions':
                                        ("Завийте <b>надясно</b> "
                                            "на <b>бул. „Витоша“</b>")
                                },
                                {
                                    'html_instructions':
                                        ("Завийте <b>наляво</b>"
                                            " на <b>ул. „Верила“</b>")
                                },
                                {
                                    'html_instructions':
                                        ("Завийте <b>надясно</b> на <b>"
                                            "ул. „Цар Асен I-ви“</b>")

                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.expected = '''Завийте надясно на бул. „Витоша“
Завийте наляво на ул. „Верила“
Завийте надясно на ул. „Цар Асен I-ви“'''

        self.landmarks = []
        self.landmarks.append(Landmark("Едно", 123, 456))
        self.landmarks.append(Landmark("Две", 123, 456))
        self.landmarks.append(Landmark("Три", 123, 456))

        self.landmarks[0].set_forecast_data(60, 10)
        self.landmarks[0].set_travel_duration(15000)

        self.landmarks[1].set_forecast_data(0, 25)
        self.landmarks[1].set_travel_duration(4000)

        self.landmarks[2].set_forecast_data(30, 20)
        self.landmarks[2].set_travel_duration(8000)

        self.expected_sorted = [self.landmarks[1],
                                self.landmarks[2],
                                self.landmarks[0]]

    def test_removing_html(self):
        self.assertEqual(
            self.expected,
            googlish.directions_and_durations.transform_html_directions(
                self.sample_response))

    def test_sorting(self):
        self.assertEqual(sort_landmarks(self.landmarks), self.expected_sorted)

if __name__ == '__main__':
    unittest.main()
