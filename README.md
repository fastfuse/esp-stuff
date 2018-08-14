### ESP8266 snippets and tricks

#### Tools

* esptool
* [ampy](https://github.com/adafruit/ampy)


#### Workflow:

* Write Python code on your computer using your favorite text editor.
* Structure the code so it puts setup code at the top and loop code inside a main loop.
* Use the `ampy run` command with the `--no-output` option to run the script on the MicroPython board.
* Edit and run the script as much as you need for it to work the way you expect.
* When you want the code to automatically run on boot use the `ampy put` command to save the script as a `/main.py` file on the board.

```sh
$> ampy --port /serial/port put test.py /main.py
```
