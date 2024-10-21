from typing import List
import requests
from Bio import Entrez

def get_citations(doi:str) -> str:
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        references = data.get("message", {}).get("reference", [])
        return ", ".join([ref.get('DOI', 'Unknown DOI') for ref in references])
    else:
        print(f"Error: {response.status_code}")
        return ""
    
#TODO: the mail should be a venv variable
def get_title_abstract(pmid: str) -> str:

    Entrez.email = 'hui.song@sintef.no' 
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    records = Entrez.read(handle)
    handle.close()
    
    # Step 3: Parse the XML to extract title and abstract
    article = records['PubmedArticle'][0]['MedlineCitation']['Article']
    
    # Extract the title
    title = article.get('ArticleTitle', 'No title available.')
    
    # Extract the abstract
    abstract_paragraphs = article.get('Abstract', {}).get('AbstractText', [])
    
    if isinstance(abstract_paragraphs, list):
        abstract = ' '.join(str(para) for para in abstract_paragraphs)
    else:
        abstract = str(abstract_paragraphs)
    
    return "Title: {} \nAbstract: {}".format(title, abstract)


def get_pmid_from_doi(doi: str)->str:

    Entrez.email = 'hui.song@sintef.no'  

    handle = Entrez.esearch(db='pubmed', term='"{}" [DOI]'.format(doi))
    record = Entrez.read(handle)
    handle.close()

    pmid_list = record.get('IdList', [])

    if pmid_list:
        return pmid_list[0]
    else:
        return 'No PMID found for DOI: {}'.format(doi)
    
def get_pmid_from_title(title:str)->str:
    """
    Searches PubMed for a paper by title and returns the PMID.

    Parameters:
    title (str): The title of the paper.

    Returns:
    str: The PMID of the paper if found.
    """
    # Set your email (required by NCBI)
    Entrez.email = "hui.song@sintef.no"  # Replace with your email address

    # Search for the paper using its title
    search_handle = Entrez.esearch(db="pubmed", term=title, retmode="xml")
    search_results = Entrez.read(search_handle)
    search_handle.close()

    # Get the list of PubMed IDs
    id_list = search_results.get("IdList", [])

    if not id_list:
        print("No articles found with the given title.")
        return ""
    else:
        # Return the first PMID (assuming it's the most relevant)
        return id_list[0]

def get_doi_from_pmid(pmid:str)->str:
    """
    Fetches the DOI of a paper given its PMID.

    Parameters:
    pmid (str): The PubMed ID of the paper.

    Returns:
    str or None: The DOI of the paper if found, else None.
    """
    # Set your email (required by NCBI)
    Entrez.email = "hui.song@sintef.no"  # Replace with your email address

    # Fetch the article details
    fetch_handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    fetch_results = Entrez.read(fetch_handle)
    fetch_handle.close()

    # Extract the DOI from the article data
    try:
        article = fetch_results['PubmedArticle'][0]
        article_ids = article['PubmedData']['ArticleIdList']

        for id_element in article_ids:
            if id_element.attributes.get('IdType') == 'doi':
                return str(id_element)
        print("DOI not found in the article data.")
        return ""
    except (IndexError, KeyError) as e:
        print(f"Error retrieving DOI: {e}")
        return ""
    
### This function has some problem and are currently not used ###
def get_citations_pubmed(pmid:str)->str:
    Entrez.email = "hui.song@sintef.no"
    links = Entrez.elink(dbfrom="pubmed", id=pmid, linkname="pubmed_pubmed_refs")
    record = Entrez.read(links)
	
    records = record[0][u'LinkSetDb'][0][u'Link']
    link_list = []
    for link in records:
        link_list.append(link[u'Id'])

    print(link_list)
    for index, id in enumerate(link_list):
        print(id)
        handle = Entrez.efetch(db='pubmed', id=id, retmode='xml')
        records = Entrez.read(handle)
        handle.close()
    
    # Step 3: Parse the XML to extract title and abstract
        article = records['PubmedArticle'][0]['MedlineCitation']['Article']
    
    # Extract the title
        title = article.get('ArticleTitle', 'No title available.')
        print(index, title)

# Function to fetch references from CrossRef using DOI
def get_references(doi) -> List[str]:
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        references = data.get("message", {}).get("reference", [])
        return [ref.get('DOI', 'Unknown DOI') for ref in references]
    else:
        print(f"Error: {response.status_code}")
        return []

### The following two functions are not necessary (the agents can figure out by itself how to combine the functions),
### but it will help save some tokens.
def get_title_abstract_from_doi(doi:str)->str:
    pmid = get_pmid_from_doi(doi)
    return get_title_abstract(pmid)

def get_doi_from_title(title:str)->str:
    pmid = get_pmid_from_title(title)
    return get_doi_from_pmid(pmid)