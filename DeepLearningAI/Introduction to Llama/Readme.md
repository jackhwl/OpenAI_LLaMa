1. Understanding the Llama Family
    - Exploring Llama's Evolution
      - Llama 1 Feb 2023
      - Llama 2 Jul 2023, commercial license: 700M monthly active users
      - Llama 3 Apr 2024 
      - Llama 3.1 Jul 2024, 8B, 70B, 405B

      ```
      wenlin.huang@MBNA-L0WXYP7D0W ~ % ollama show llama3:latest
        Model
            architecture        llama    
            parameters          8.0B     
            context length      8192     
            embedding length    4096     
            quantization        Q4_0     

        Capabilities
            completion    

        Parameters
            num_keep    24                       
            stop        "<|start_header_id|>"    
            stop        "<|end_header_id|>"      
            stop        "<|eot_id|>"             

        License
            META LLAMA 3 COMMUNITY LICENSE AGREEMENT             
            Meta Llama 3 Version Release Date: April 18, 2024    
            ...                                                 
      ```
      - Llama 3.2 Sep 2024
      - Llama 3.3 Dec 2024
      - Llama 4 Apr 2025
    - Comparing Llama Models
      - Llama 3.1 8B
        - context window of about 100 pages of text
        - Benchmark Scores
          - Llama 3.1 8B 70%
          - ChatGPT 3.5 70%
          - Llama 3.1 70B 85%
          - ChatGPT 5 90%