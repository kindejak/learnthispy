import difflib

"""
function to compare two texts (lists of strings) and return diff
"""
def compare_texts(text1, text2):
    # convert to lists of lines
    text1 = text1.splitlines()
    text2 = text2.splitlines()
    # compare
    return "".join(difflib.HtmlDiff().make_table(text1, text2, context=False, numlines=0))

if __name__ == "__main__":
    text1 = "hello\n world\n"
    text2 = "hello\n world"
    print(compare_texts(text1, text2))