import unittest

import adventure


class AdventureTests(unittest.TestCase):
    def play_with(self, answers, seed=7):
        remaining = iter(answers)
        output = []
        endings = adventure.play_game(
            seed=seed,
            input_fn=lambda _prompt: next(remaining),
            output_fn=output.append,
        )
        return endings, output

    def test_forest_path_reaches_village_ending(self):
        endings, _ = self.play_with(["1", "1", "1", "1", "1", "n"])
        self.assertEqual(endings, ["end_village"])

    def test_bridge_path_reaches_rescue_ending(self):
        endings, _ = self.play_with(["2", "1", "1", "1", "n"])
        self.assertEqual(endings, ["end_rescue"])

    def test_invalid_choice_is_reasked(self):
        endings, output = self.play_with(["x", "3", "2", "2", "1", "1", "n"])
        self.assertEqual(endings, ["end_cliff"])
        self.assertEqual(
            sum("Please enter a number from 1 to 2." in line for line in output),
            2,
        )

    def test_seed_repeats_random_event(self):
        _, first_output = self.play_with(["1", "1", "1", "1", "1", "n"], seed=19)
        _, second_output = self.play_with(["1", "1", "1", "1", "1", "n"], seed=19)
        event_lines = [
            line for line in first_output if line in adventure.RANDOM_EVENTS["ridge_weather"]
        ]
        repeated_event_lines = [
            line
            for line in second_output
            if line in adventure.RANDOM_EVENTS["ridge_weather"]
        ]
        self.assertEqual(event_lines, repeated_event_lines)
        self.assertEqual(len(event_lines), 1)

    def test_play_again_restarts_at_start(self):
        endings, output = self.play_with(
            ["1", "1", "1", "1", "1", "y", "2", "1", "1", "1", "n"]
        )
        self.assertEqual(endings, ["end_village", "end_rescue"])
        self.assertEqual(sum("Dusk settles over the mountain." in line for line in output), 2)


if __name__ == "__main__":
    unittest.main()
