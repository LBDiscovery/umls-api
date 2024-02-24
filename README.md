# umls-api

Class to interact with the UMLS API

- Documentation will be added later, for now refer to the [APIs](https://documentation.uts.nlm.nih.gov/rest/home.html) documentation. Each endpoint maps to a function in the class.

## Installation

```
pip install umls-api-client
```

## Usage

```
from umls_api_client import UMLS
umls = UMLS.UMLS('ENTER YOUR UMLS API KEY')

data = umls.retrieve_cuis(['D003160', 'D016430', 'D052061', 'D013487', 'D013485'],inputType='code')

data2 = umls.retrieve_cuis('D003160',inputType='code')
```


## Credits

- **Author:** Naveen Jayakody
- **UMLS Citation**:
  - Bodenreider O. The Unified Medical Language System (UMLS): integrating biomedical terminology. Nucleic Acids Res. 2004 Jan 1;32(Database issue):D267-70. doi: 10.1093/nar/gkh061. PubMed PMID: 14681409; PubMed Central PMCID: PMC308795.
  - [Read the full text](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC308795/)
  - [UMLS API Technical Documentation](https://documentation.uts.nlm.nih.gov/rest/home.html)


