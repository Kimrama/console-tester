# To use this program
You have to put **test.exe** and **test_set.json** at the same directory with files which you want to test
```
root(working folder)
┣ q1.py
┣ q2.py
┣ ....py
┣ test.exe
┗ test_set.json
```

## Drag and Drop Function
You can simply drag the Python source file `.py` with same set_name provided in `test_set.json` on to the executable `.exe` to automatically test that script.
<center>
  <img src="./docs/media/drag_n_drop.gif" alt="" style="width:50%;"/>
</center>

### About test_set.json
test_set.json use to store test set data in array of json
```json
[
  {
    "setname": string,
    "describe": string,
    "testcase": [object]
  },
  {
    "setname": "set1",
    "describe": "this set use with question 1",
    "testcase": [
                  {
                    "input": "3 2",
                    "expected_output": "5"
                  },
                  {
                    "input": "4 1",
                    "expected_output": "5"
                  },
                ]
  },
]
```
### so you can edit your test in this

