# Social-Media-Data-Analysis

This repository contains the PyCharm project code I used for a set of Meta chat data analysis and presentation scripts. Specifically, these scripts perform anaylsis for both Facebook and Instagram. There are two scripts in this project; one for processing the data, one for presenting the data. The process is as follows:
- Iterate through the downloaded data directories and find all the JSON data files for each chat in the user's chat history.
- Import the JSON data into a big awful dictionary, keyed by the platform and chat.
- Iterate over the big-awful-dictionary and collect some statistics for each chat.
- Embed statistics for each chat back into the big-awful-dictionary.
- Export big-awful-dictionary into a JSON file in the "output" folder.

Following this the data is presented as follows:
- Setup a Plotly Dash web-app.
- Create a simple HTML structure for the to allow the user to choose which platform and chat they access.
- Provide various tables and graphs to display the data analysis results for the selected chat.

## Project Structure

```
├── ""config"" => Contains configuration files for this project.
├── ""output"" => Contains results of the data analysis in JSON format or other CSV files will be output here.  
├── ""src"" => Contains the source code for this project.
│    ├── ""assets"" => Contains the CSS files for the web app. 
│    ├── ""data_pres.py"" => The Python script that uses Plotly Dash to present the data analysis results.  
│    ├── ""hex_to_TB.py"" => The Python sript that imports the raw chat message data and provides a data analysis.
```