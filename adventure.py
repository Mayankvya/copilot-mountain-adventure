"""A small, data-driven mountain-hiking adventure."""

import argparse
import random


SCENES = {
    "start": {
        "text": (
            "Dusk settles over the mountain. You have lost the marked path, "
            "and the valley is somewhere below."
        ),
        "choices": [
            ("Follow a faint trail through the pines", "trail"),
            ("Head downhill toward the sound of water", "creek"),
        ],
    },
    "trail": {
        "text": "The faint trail bends around a stand of pines and reaches a fork.",
        "choices": [
            ("Look for a marker on the rocky rise", "marker"),
            ("Take a narrow track into the ravine", "ravine"),
        ],
    },
    "creek": {
        "text": "A cold creek cuts across your way downhill.",
        "choices": [
            ("Search upstream for a footbridge", "bridge"),
            ("Try the rough crossing downstream", "ford"),
        ],
    },
    "marker": {
        "text": "A weathered trail marker points toward a ridge and a small shelter.",
        "choices": [
            ("Climb toward the ridge", "ridge"),
            ("Make for the shelter", "hut"),
        ],
    },
    "ravine": {
        "text": "The ravine is steep, but a line of old cairns shows a way through.",
        "choices": [
            ("Follow the cairns up to the ridge", "ridge"),
            ("Turn back toward the creek", "creek"),
        ],
    },
    "bridge": {
        "text": "You find a narrow footbridge, still solid beneath your boots.",
        "choices": [
            ("Cross and follow the path to a shelter", "hut"),
            ("Cross toward the ridge above the trees", "ridge"),
        ],
    },
    "ford": {
        "text": "The water is swift here. You spot a rocky bank near a distant cascade.",
        "choices": [
            ("Pick your way toward the cascade", "falls"),
            ("Climb back toward the ridge", "ridge"),
        ],
    },
    "hut": {
        "text": (
            "A small ranger shelter offers a dry place to rest. "
            "A trail sign is just visible in the fading light."
        ),
        "choices": [
            ("Follow the sign downhill", "end_rescue"),
            ("Take the rough path back to the ridge", "ridge"),
        ],
    },
    "ridge": {
        "text": (
            "At the ridge, you can see a dark forest below and the outline "
            "of a shelter behind you."
        ),
        "event": "ridge_weather",
        "choices": [
            ("Descend through the forest", "forest"),
            ("Return to the shelter", "hut"),
        ],
    },
    "falls": {
        "text": "The cascade is louder now, and its slick rocks fall away into darkness.",
        "choices": [
            ("Try to cross on the wet rocks", "end_cliff"),
            ("Retreat and climb toward the ridge", "ridge"),
        ],
    },
    "forest": {
        "text": "Below the ridge, a broad path winds through the trees toward distant lights.",
        "choices": [
            ("Keep following the lights", "end_village"),
            ("Turn back for the shelter", "hut"),
        ],
    },
    "end_village": {
        "text": (
            "You reach the village as the last light fades. Warm windows "
            "and a safe trail are ahead. You made it down the mountain."
        ),
        "ending": True,
    },
    "end_rescue": {
        "text": (
            "The marked trail leads to a ranger station. The ranger gets you "
            "inside just as night falls. You are safe."
        ),
        "ending": True,
    },
    "end_cliff": {
        "text": (
            "A rock shifts underfoot. You grab a root and stop yourself from "
            "sliding, but the crossing is impossible in the dark. A rescue "
            "team finds you at first light."
        ),
        "ending": True,
    },
}

RANDOM_EVENTS = {
    "ridge_weather": (
        "A gust lifts the mist, briefly revealing a line of trail markers.",
        "Fog rolls over the ridge, making every step feel uncertain.",
    ),
}


def _ask_choice(scene, input_fn, output_fn):
    choices = scene["choices"]
    for number, (label, _) in enumerate(choices, start=1):
        output_fn(f"{number}. {label}")

    while True:
        answer = input_fn("Choose a path: ").strip()
        try:
            number = int(answer)
        except ValueError:
            number = 0
        if 1 <= number <= len(choices):
            return choices[number - 1][1]
        output_fn(f"Please enter a number from 1 to {len(choices)}.")


def _ask_play_again(input_fn, output_fn):
    while True:
        answer = input_fn("Play again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        output_fn("Please answer y or n.")


def play_game(seed=None, input_fn=None, output_fn=None):
    """Play until the player declines a replay; return the ending scene IDs."""
    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print

    rng = random.Random(seed)
    endings = []
    while True:
        current = "start"
        while not SCENES[current].get("ending"):
            scene = SCENES[current]
            output_fn(f"\n{scene['text']}")
            event = scene.get("event")
            if event is not None:
                output_fn(rng.choice(RANDOM_EVENTS[event]))
            current = _ask_choice(scene, input_fn, output_fn)

        output_fn(f"\n{SCENES[current]['text']}")
        endings.append(current)
        if not _ask_play_again(input_fn, output_fn):
            return endings


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Find your way down the mountain before nightfall."
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="integer seed for repeatable random events",
    )
    args = parser.parse_args(argv)
    play_game(seed=args.seed)


if __name__ == "__main__":
    main()
