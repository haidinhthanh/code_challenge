#project link 

- https://github.com/haidinhthanh/code_challenge.git

#setup enviroment:

1.linux:
Run flow command:
    * Install enviroment
        -   cd code_challenge
        -   python3 -m virtualenv venv
        -   . venv/bin/activate
    * Upgrade pip:
        -   python3 -m pip install --upgrade pip
    * Install package:
        -   pip install -r requirements.txt

        
2.setup flask:
Run flow command:
    
    * Create .env file
        -   cd bin    
        -   touch .env
    * Edit .env with content:

        FLASK_APP=main.py
        FLASK_ENV=development
    

    
#runing task

1.task 1: word counter
Run flow command:
Count word from file
    -   python3 bin/word_counter.py -p path -t type
    * path: absolute file path *
    * type: type sort asc|desc

Test count word
    -   python3 -m unittest bin/word_counter_test.py
    
2.task 2: 

2.1 crawler news from vnexpress

Setup elastic search:
Run flow command:
start 
    -   curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.2-linux-x86_64.tar.gz
    -   tar -xvf elasticsearch-7.9.2-linux-x86_64.tar.gz
    -   cd elasticsearch-7.9.2
    -   ./bin/elasticsearch -d -p pid

kill:
    -   pkill -F pid
    
2.2 Crawl newspaper
Run flow command:
    -   cd newspaper_crawl:
    -   scrapy crawl vn_express_url_crawler
    -   scrapy crawl vn_express_spider

2.2 flask server
    -   cd bin

    -   flask run
    
    
