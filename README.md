# Setup
Make sure you have python 3.8 and pip installed, or alternatively miniconda3.
Create a conda environment and activate it.
run "pip install -r requirements.txt"

## Running the program
Navigate to the perseuss directory and run the following command:
python app.py

## Testing
python -m pytest

## Docker
docker build --tag=name_of_the_app
docker run -p 5000:5000 name_of_the_app

## example payload for request
data=json.dumps({
            "jsonrpc": "2.0",
            "method": "classify",
            "params": {"Pclass": 1, "Sex": "female", "Age": 34, "SibSp": 1, "Parch": 0, "Embark": "S"},
            "id": "1"
        }),
        content_type='application/json',
    )
    
    
## Future improvements:
1) Deploy app on kubernetes cluster to scale up.
2) Implement better logging (and save logs to file) for improved traceability.
