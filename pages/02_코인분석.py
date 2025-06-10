ValueError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/secondproject/pages/02_코인분석.py", line 76, in <module>
    data = pd.DataFrame(all_crypto_data)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/frame.py", line 778, in __init__
    mgr = dict_to_mgr(data, index, columns, dtype=dtype, copy=copy, typ=manager)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/internals/construction.py", line 503, in dict_to_mgr
    return arrays_to_mgr(arrays, columns, index, dtype=dtype, typ=typ, consolidate=copy)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/internals/construction.py", line 114, in arrays_to_mgr
    index = _extract_index(arrays)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/core/internals/construction.py", line 667, in _extract_index
    raise ValueError("If using all scalar values, you must pass an index")
