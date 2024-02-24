import requests
from ratelimit import limits, sleep_and_retry
from concurrent.futures import ThreadPoolExecutor

REQ_PER_SEC=15

class UMLS:
    

    def __init__(self, api_key:str, requests_per_second:int=20):
        self._api_key = api_key
        self._base_url = "https://uts-ws.nlm.nih.gov/rest"
        self._requests_per_second = requests_per_second 
        self.REQ_PER_SEC=self._requests_per_second        
    

    def retrieve_cui_atoms(self, cui_list:list[str], version:str='current', preferred:bool=False,includeObsolete:bool=True,includeSuppressible:bool=True,sabs:list[str]=[],language:str='',ttys:list[str]=[]
                          ,pageNumber:int=1,pageSize:int=25):
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        if (len(sabs)==1):
            params["sabs"] = sabs[0]
        elif(len(sabs)>1):
            sabsString = ','.join(sabs)
            params["sabs"] = sabsString

        if (len(ttys)==1):
            params["ttys"] = ttys[0]
        elif(len(ttys)>1):
            ttysString = ','.join(ttys)
            params["ttys"] = ttysString
        
        if (includeObsolete):
            params["includeObsolete"] = 'true'
        else:
            params["includeObsolete"] = 'false'

        if (includeSuppressible):
            params["includeSuppressible"] = 'true'
        else:
            params["includeSuppressible"] = 'false'

        if (language != ''):
            params['language'] = language


        headers = {"Content-Type": "application/x-www-form-urlencoded"}
      
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_cui_atom(cui):

            search_endpoint = f"{self._base_url}/content/{version}/CUI/{cui}/atoms"
            if preferred:
                search_endpoint += "/"+"preferred"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_cui_atom,cui): cui for cui in cui_list}
            results = {cui: future.result() for future, cui in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
        

    def retrieve_cui_definitions(self, cui_list:list[str], version:str='current',sabs:list[str]=[], pageNumber:int=1, pageSize:int=25):
        
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        if (len(sabs)==1):
            params["sabs"] = sabs[0]
        elif(len(sabs)>1):
            sabsString = ','.join(sabs)
            params["sabs"] = sabsString


        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_cui_definition(cui):
            search_endpoint = f"{self._base_url}/content/{version}/CUI/{cui}/definitions"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_cui_definition,cui): cui for cui in cui_list}
            results = {cui: future.result() for future, cui in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
        
    def retrieve_cui_relations(self, cui_list:list[str], version:str='current', includeRelationLabels:list[str]=[],includeAdditionalRelationLabels:list[str]=[],includeObsolete:bool=False,includeSuppressible:bool=False,sabs:list[str]=[]
                          ,pageNumber:int=1,pageSize:int=25):
        
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        if (len(sabs)==1):
            params["sabs"] = sabs[0]
        elif(len(sabs)>1):
            sabsString = ','.join(sabs)
            params["sabs"] = sabsString
        
        if (len(includeRelationLabels)==1):
            params["includeRelationLabels"] = includeRelationLabels[0]
        elif(len(includeRelationLabels)>1):
            labels = ','.join(includeRelationLabels)
            params["includeRelationLabels"] = labels
        
        if (len(includeAdditionalRelationLabels)==1):
            params["includeAdditionalRelationLabels"] = includeAdditionalRelationLabels[0]
        elif(len(includeAdditionalRelationLabels)>1):
            labels = ','.join(includeAdditionalRelationLabels)
            params["includeAdditionalRelationLabels"] = labels
        
        if (includeObsolete):
            params["includeObsolete"] = 'true'
        else:
            params["includeObsolete"] = 'false'

        if (includeSuppressible):
            params["includeSuppressible"] = 'true'
        else:
            params["includeSuppressible"] = 'false'


        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_cui_relations(cui):
            search_endpoint = f"{self._base_url}/content/{version}/CUI/{cui}/relations"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_cui_relations,cui): cui for cui in cui_list}
            results = {cui: future.result() for future, cui in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
        
    def retrieve_source_asserted_id_info(self,id_list:list[str],source:str,version:str='current'):
        params = {
            "apiKey": self._api_key,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_info(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_info,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results


    def retrieve_source_asserted_id_atoms(self,id_list:list[str],source:str,version:str='current'):
        params = {
            "apiKey": self._api_key,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}


        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_info(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/atoms"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_info,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    
    def retrieve_source_asserted_id_parents(self,id_list:list[str],source:str,version:str='current',pageNumber:int=1,pageSize:int=25):
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_parents(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/parents"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_parents,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    
    def retrieve_source_asserted_id_children(self,id_list:list[str],source:str,version:str='current',pageNumber:int=1,pageSize:int=25):
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_children(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/children"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_children,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results

    def retrieve_source_asserted_id_ancestors(self,id:str,source:str,version:str='current',pageNumber:int=1,pageSize:int=25):
        search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/ancestors"
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_ancesstors(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/ancestors"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_ancesstors,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    
    def retrieve_source_asserted_id_descendants(self,id_list:list[str],source:str,version:str='current',pageNumber:int=1,pageSize:int=25):
       
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_descendants(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/descendants"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_descendants,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
        
    def retrieve_source_asserted_id_relations(self,id_list:list[str],source:str,version:str='current',pageNumber:int=1,pageSize:int=25,
                                              includeRelationLabels:list[str]=[],includeAdditionalRelationLabels:list[str]=[],includeObsolete:bool=False,includeSuppressible:bool=False):
        
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        if (len(includeRelationLabels)==1):
            params["includeRelationLabels"] = includeRelationLabels[0]
        elif(len(includeRelationLabels)>1):
            labels = ','.join(includeRelationLabels)
            params["includeRelationLabels"] = labels
        
        if (len(includeAdditionalRelationLabels)==1):
            params["includeAdditionalRelationLabels"] = includeAdditionalRelationLabels[0]
        elif(len(includeAdditionalRelationLabels)>1):
            labels = ','.join(includeAdditionalRelationLabels)
            params["includeAdditionalRelationLabels"] = labels
        
        if (includeObsolete):
            params["includeObsolete"] = 'true'
        else:
            params["includeObsolete"] = 'false'

        if (includeSuppressible):
            params["includeSuppressible"] = 'true'
        else:
            params["includeSuppressible"] = 'false'


        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_relations(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/relations"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_relations,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
        
    def retrieve_source_asserted_id_attributes(self,id_list:list[str],source:str,version:str='current',pageNumber:int=1,pageSize:int=25,includeAttributeNames:list[str]=[]):
        
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }

        if (len(includeAttributeNames)==1):
            params["includeAttributeNames"] = includeAttributeNames[0]
        elif(len(includeAttributeNames)>1):
            labels = ','.join(includeAttributeNames)
            params["includeAttributeNames"] = labels
        
      
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_source_asserted_id_attributes(id):
            search_endpoint = f"{self._base_url}/content/{version}/source/{source}/{id}/attributes"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_source_asserted_id_attributes,id): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    
    def retrieve_tui_info(self,tui_list:list[str],version:str='current'):
        
        params = {
            "apiKey": self._api_key,
        }    
            
      
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_tui_info(tui):
            search_endpoint = f"{self._base_url}/semantic-network/{version}/TUI/{tui}"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_tui_info,tui): tui for tui in tui_list}
            results = {tui: future.result() for future, tui in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    
    @limits(calls=REQ_PER_SEC, period=1)
    def crosswalk_vocabs_using_cuis(self,cui_list:list[str],source:str,version:str='current',targetSource:list[str]=[],includeObsolete:bool=False,pageNumber:int=1,pageSize:int=25):
        
        params = {
            "apiKey": self._api_key,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
        }    

        if (len(targetSource)==1):
            params["targetSource"] = targetSource[0]
        elif(len(targetSource)>1):
            targetSourceString = ','.join(targetSource)
            params["includeAdditionalRelationLabels"] = targetSourceString
        
        if (includeObsolete):
            params["includeObsolete"] = 'true'
        else:
            params["includeObsolete"] = 'false'
      
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_crosswalk_vocabs_using_cui(cui):
            search_endpoint = f"{self._base_url}/crosswalk/{version}/source/{source}/{cui}"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_crosswalk_vocabs_using_cui,cui): cui for cui in cui_list}
            results = {cui: future.result() for future, cui in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    
    def retrieve_cuis(self, id_list:list[str], version:str='current',inputType:str='atom',includeObsolete:bool=False,includeSuppressible:bool=False,returnIdType:str='concept',sabs:list[str]=[],
                     searchType:str='words',partialSearch:bool=False,pageNumber:int=1,pageSize:int=25):
        search_endpoint = f"{self._base_url}/search/{version}"

        params = {
            "apiKey": self._api_key,
            "inputType":inputType,
            "searchType":searchType,
            "pageNumber":pageNumber,
            "pageSize":pageSize,
            "returnIdType":returnIdType
        }

        if (includeObsolete):
            params["includeObsolete"] = 'true'
        else:
            params["includeObsolete"] = 'false'

        if (includeSuppressible):
            params["includeSuppressible"] = 'true'
        else:
            params["includeSuppressible"] = 'false'

        if (partialSearch):
            params["partialSearch"] = 'true'
        else:
            params["partialSearch"] = 'false'
        
        if (len(sabs)==1):
            params["sabs"] = sabs[0]
        elif(len(sabs)>1):
            sabsString = ','.join(sabs)
            params["sabs"] = sabsString

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_cui(id, params_local):
            params_local["string"] = id
            response = requests.get(search_endpoint, params=params_local,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_cui,id,params.copy()): id for id in id_list}
            results = {id: future.result() for future, id in futures.items()}
            # ordered_results = [results[id] for id in id_list]
        return results
    

    def retrieve_cui_info(self, cui_list:list[str], version:str='current'):
        
        params = {"apiKey":self._api_key}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        @sleep_and_retry
        @limits(calls=self.REQ_PER_SEC, period=1)
        def fetch_cui_info(cui):
            search_endpoint = f"{self._base_url}/content/{version}/CUI/{cui}"
            response = requests.get(search_endpoint, params=params,headers=headers)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(fetch_cui_info,cui): cui for cui in cui_list}
            results = {cui: future.result() for future, cui in futures.items()}
            # ordered_results = [results[cui] for cui in cui_list]
        return results
    
        