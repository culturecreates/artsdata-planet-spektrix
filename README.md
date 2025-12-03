# artsdata-planet-spektrix

For the project report, client guidelines and instructions for Artsdata data stewards, see [this Google Directory](https://drive.google.com/drive/folders/1ulghARz9p94jltlJj1RlyAyVZKRD-ZYo?usp=drive_link). The document [Process for Loading a Spektrix Client to Artsdata](https://docs.google.com/document/d/1NoKqk1tHyiesAlbtrPBrKII5H_FwW0NwbsyV-X8yqwY/edit?usp=sharing) includes step-by-step instructions for Artsdata data stewards.


Manual Workflow
--------------

You can run a single source like 'manitobaopera' by going to the [Actions tab](https://github.com/culturecreates/artsdata-planet-spektrix/actions/workflows/fetch-data-and-push.yml) and using the button "Run workflow" and inputing 'manitobaopera' into the field to search data from.

columns.json
-

[Columns.json](https://github.com/culturecreates/artsdata-planet-spektrix/blob/main/ontorefine/columns.json) contains columns that need to be added to the [ontorefine configuration](https://github.com/culturecreates/artsdata-planet-spektrix/blob/main/ontorefine/configuration.json) before the transformation. As we are working with multiple sources with a single ontorefine configuration and each source can have optional fields, it is necessary that this file should be updated on each additional source, so that the other sources are not affected.

This project uses a shared [ontorefine configuration](https://github.com/culturecreates/artsdata-planet-spektrix/blob/main/ontorefine/configuration.json) that is applied to multiple spektrix sources. Since each source may contain different sets of fields, we must manage optional columns carefully to ensure transformations work consistently across all datasets.

The file [columns.json](https://github.com/culturecreates/artsdata-planet-spektrix/blob/main/ontorefine/columns.json) defines the full set of columns expected by the transformation. When a new source is added that introduces additional fields, those columns **must be appended** to columns.json. Updating this file ensures that optional fields are recognized by OntoRefine prior to transformation and prevents errors or data loss for other existing sources.

columns.json structure:

    {
        "op": "core/column-addition",
        "engineConfig": {
            "facets": [],
            "mode": "row-based"
        },
        "baseColumnName": "_ - id",
        "expression": "set-to-blank",
        "onError": "set-to-blank",
        "newColumnName": <optional_column_name_here>,
        "columnInsertIndex": 1
    }


On each workflow run, the columns.json will get appended to the "operations" section of the main OntoRefine configuration file.

run_ontorefine.sh
-

This script starts the OntoRefine server for a specific Spektrix data source.
Before running the script, set the source variable inside the file to the desired Spektrix source name.

### Usage:

1. Open run_ontorefine.sh in a text editor

2. Update the value of the source variable to the source you want to process

3. Run the script: ./run_ontorefine.sh

The OntoRefine server will start and load the configuration for the selected source.

additional_info.yml
-

This configuration file is used to define source-specific attributes and dynamic URL generation logic.

### Adding a New Source

To add a new source, use the organization's slug as the top-level key. Within that key, you can define attributes such as event urls and offer urls.

### Common Attributes:

- attribute_EventUrl: The URL where the source's events are listed.
- offerUrl: The booking or purchase URL. This often uses placeholders (e.g., {webInstanceId}) or transformation functions.

### Example Configuration:

    sourcename1:
      attribute_EventUrl: "https://example.com/events1"
      offerUrl: "https://example.com/book/?id={eventId1}"

    sourcename2:
      attribute_EventUrl: "https://example.com/events2"
      offerUrl: "https://example.com/tickets/?event={eventId2}"

### Transformation Functions

You can use the following transformation functions within your URL strings to dynamically format data.

| Function                      | Description                                                                       |  Usage Example    |
| ------------------------------| --------------------------------------------------------------------------------- | -----------       |
| `extractID`                   | Extracts a numeric ID from a string (e.g., turns "instance_12345" into "12345").  | {extractID(name)} |
| `slugify`                     | Converts a string to a URL-friendly slug (e.g., turns "My Event" into "my-event").| {slugify(name)}   |

#### Advanced slugify Usage

The slugify function accepts additional arguments to customize the output.
> Note: Additional arguments must be passed as named arguments.

Example:

    offerUrl: "https://site.com/events/{slugify(name, remove_words=['the', 'over'])}"