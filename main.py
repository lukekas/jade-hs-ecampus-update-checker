from dotenv import load_dotenv
import os
import sys
import requests
import xml.dom.minidom
import xml
from time import sleep

def get_url() -> str:
  if not load_dotenv():
    print(".env not found")
    sys.exit()

  if os.environ.get("URL") == None or os.environ.get("URL") == "":
    print("URL is not given")
    sys.exit()

  return os.environ.get("URL")

def get_xml(url) -> str:
  r = requests.get(url)
  if r.status_code != 200:
    print("URL does not seem to be correct")
    sys.exit()

  return r.text

def recursive_clean(elem) -> None:
  if elem.tagName == "dc:date":
    elem.parentNode.removeChild(elem)
    return

  for ch in elem.childNodes:
    if isinstance(ch, xml.dom.minidom.Element):
      recursive_clean(ch)

def clean_dom(dom):
  dom = dom.replace('\n', "")
  doc = xml.dom.minidom.parseString(dom)
  recursive_clean(doc.firstChild)
  
  return doc

def get_cleaned_doc_string(url) -> str:
  dom_string = get_xml(url)
  dom = clean_dom(dom_string)
  return dom.toprettyxml()

def iterate_until_changes(url) -> bool:
  version_old = get_cleaned_doc_string(url)

  while True:
    version_new = get_cleaned_doc_string(url)
    if (version_old != version_new):
      return True

    version_old = version_new
    sleep(60)
    

if __name__ == "__main__":
  url = get_url()
  
  if iterate_until_changes(url) == True:
    print("Changes!")