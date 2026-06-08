# %%
import pandas as pd
import random
from datetime import date
import streamlit as st

# %%
filename = "iec_work.xlsx"
gym_opts = pd.read_excel(filename, sheet_name="Gym")
swim_opts = pd.read_excel(filename, sheet_name="Swim")

# %% [markdown]
# GYM WORKOUT

# %%
def create_gym_workout(gym_opts):
    def grouping(gym_opts):
        grouped_by_level = gym_opts.groupby("Level")
        warmup = grouped_by_level.get_group("Warmup")
        core = grouped_by_level.get_group("Core")
        arms = grouped_by_level.get_group("Arms")
        legs = grouped_by_level.get_group("Legs")
        return warmup, core, arms, legs
    warmup, core, arms, legs = grouping(gym_opts)

    def pick_gym_workout(warmup, core, arms, legs):
        random_warmup = warmup.sample(2)
        random_core = core.sample(3)
        random_arms = arms.sample(3)
        random_legs = legs.sample(3)
        gym_workout = pd.concat([random_warmup, random_core, random_arms, random_legs])
        gym_workout["Reps"] = gym_workout.apply(
            lambda row: random.randint(int(row["RandInt Min"]), int(row["RandInt Max"])), axis=1
        )
        return gym_workout
    gym_workout = pick_gym_workout(warmup, core, arms, legs)

    def format_workout(gym_workout):
        output = ""
        level_order = ["Warmup", "Core", "Arms", "Legs"]
        sets = {"Warmup": 2, "Core": 3, "Arms": 3, "Legs": 3}

        for level in level_order:
            group = gym_workout[gym_workout["Level"] == level]

            output += f"\n{'='*5} {level.upper()} {'='*5}\n\n"

            exercises = list(group.iterrows())
            mid = len(exercises) // 2
            num_sets = sets[level]

            output += "        —\n"
            for i, (_, row) in enumerate(exercises):
                reps = row["Reps"]
                exercise = row["Set"]
                if i == mid:
                    output += f"{num_sets}x | {reps} {exercise}\n"
                else:
                    output += f"   | {reps} {exercise}\n"
            output += "        —\n"

        return output

    return format_workout(gym_workout)


# %% [markdown]
# SWIM WORKOUT

# %%
def create_swim_workout(swim_opts):
    def grouping(swim_opts):
        grouped_by_level = swim_opts.groupby("Level")
        warmup = grouped_by_level.get_group("Warmup")
        grouped_by_type = warmup.groupby("Workout Type")
        swim_warmup = grouped_by_type.get_group("Swim")
        kick_warmup = grouped_by_type.get_group("Kick")
        pull_warmup = grouped_by_type.get_group("Pull")
        var_warmup = grouped_by_type.get_group("Variable")
        preset = grouped_by_level.get_group("Preset")
        main = grouped_by_level.get_group("Main")
        warmdown = grouped_by_level.get_group("Warmdown")
        return swim_warmup, kick_warmup, pull_warmup, var_warmup, preset, main, warmdown
    swim_warmup, kick_warmup, pull_warmup, var_warmup, preset, main, warmdown = grouping(swim_opts)

    def pick_swim_workout(swim_warmup, kick_warmup, pull_warmup, var_warmup, preset, main, warmdown):
        random_swim_warmup = swim_warmup.sample(1)
        random_kick_warmup = kick_warmup.sample(1)
        random_pull_warmup = pull_warmup.sample(1)
        random_var_warmup = var_warmup.sample(1)
        random_preset = preset.sample(1)
        random_main = main.sample(1)
        random_warmdown = warmdown.sample(1)
        swim_workout = pd.concat([random_swim_warmup, random_kick_warmup, random_pull_warmup,
                                   random_var_warmup, random_preset, random_main, random_warmdown])
        return swim_workout
    swim_workout = pick_swim_workout(swim_warmup, kick_warmup, pull_warmup, var_warmup, preset, main, warmdown)

    def format_workout(swim_workout):
        output = ""
        level_order = ["Warmup", "Preset", "Main", "Warmdown"]
        today = date.today()
        chill = today.strftime("%A, %B %d, %Y")
        output += f"\n{'='*3} {chill} {'='*3}\n"

        for level in level_order:
            group = swim_workout[swim_workout["Level"] == level]
            if group.empty:
                continue

            exercises = list(group.iterrows())

            for _, row in exercises:
                exercise = str(row["Set"]).replace("\\n", "\n")
                rounds = int(row["Rounds"])
                lines = exercise.strip().split("\n")
                mid = len(lines) // 2

                if rounds != 1:
                    output += "        —\n"
                    for i, line in enumerate(lines):
                        if i == mid:
                            output += f"{rounds}x | {line}\n"
                        else:
                            output += f"  | {line}\n"
                    output += "        —\n\n"
                else:
                    output += f"{exercise}\n"
            output += "\n"

        return output

    return format_workout(swim_workout)


# %% [markdown]
# MAKING IT AN APP

# %%
st.title(" IEC Workout Generator")
workout_type = st.selectbox("Select Workout Type", ["Swim", "Gym"])

if st.button("Generate Workout"):
    if workout_type == "Gym":
        output = create_gym_workout(gym_opts)
    elif workout_type == "Swim":
        output = create_swim_workout(swim_opts)
    st.text(output)


