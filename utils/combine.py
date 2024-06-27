import os
import json
import argparse


def combine_predictions(dataset, model):
    # Getting a list of all prediction files
    prediction_files = [file for file in os.listdir(f"data/{dataset}/problems_{model}")
                        if file.startswith("prediction_") and file.endswith(".json")]

    # Sorting the prediction files by ID
    prediction_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

    # Reading and combining all the predictions
    combined_predictions = []
    for file in prediction_files:
        with open(os.path.join(f"data/{dataset}/problems_{model}", file), "r") as f:
            prediction = json.load(f)
            combined_predictions.append(prediction)

    # Saving the combined predictions to a file
    os.makedirs(f"predictions/{model}", exist_ok=True)
    with open(f"predictions/{model}/prediction.json", "w") as file:
        json.dump(combined_predictions, file, indent=4)

    print("Predictions combined successfully.")


def main():
    parser = argparse.ArgumentParser(description="Combine prediction files.")
    parser.add_argument("--data", type=str, default="test", help="Dataset name")
    parser.add_argument("--model", type=str, default="opus", help="Model name")
    args = parser.parse_args()

    combine_predictions(args.data, args.model)


if __name__ == "__main__":
    main()
