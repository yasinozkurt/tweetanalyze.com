from typing import NamedTuple
from flask import Flask,render_template,request
import requests
from deep_translator import GoogleTranslator
from selenium import webdriver
import time
import json
import math











app = Flask(__name__)


@app.route("/tweetanalyze", methods=['POST', 'GET'])
def tweetAnalyze():
    if request.method=="POST":
        if "text" in request.form:

            text=request.form["text"]

            if type(text)!= str:
                return render_template("tweetanalyze.html",textanalysis1="Text must contain characters, not just numbers.")
            else:
                try:

                    text=GoogleTranslator(source="auto",target="en").translate(text)

                    #burada apiye istek yolluyoruz

                    url = "https://japerk-text-processing.p.rapidapi.com/sentiment/"
                    text=text
                    if text== "":
                        text="neutral"
                    payload = "text="+text+"&language=english"
                    headers = {
                        'content-type': "application/x-www-form-urlencoded",
                        'x-rapidapi-host': "",
                        'x-rapidapi-key': ""
                        }

                    response = requests.request("POST", url, data=payload.encode("utf-8"), headers=headers)

                    dicti=json.loads(response.text)
                    label=dicti["label"]
                    if label == "pos":
                        label="POSITIVE"
                        polarityRate=dicti["probability"]["pos"]
                        polarityRate=math.floor(polarityRate*100)
                    elif label == "neg":
                        label="NEGATIVE"
                        polarityRate = dicti["probability"]["neg"]
                        polarityRate = math.floor(polarityRate * 100)
                    else:
                        label="NEUTRAL"
                        polarityRate = dicti["probability"]["neutral"]
                        polarityRate = math.floor(polarityRate * 100)

                    sent_text="Dominance: "+str(label) +" %"+str(polarityRate)




                    return render_template("tweetanalyze.html",textanalysis1=sent_text)
                except:
                    return render_template("tweetanalyze.html",textanalysis1="SOMETHİNG HAPPENED, TRY AGAİN.")








        #Twitter analyze section:
        else:

             username=request.form["username"]
             if username=="":
                 return render_template("tweetanalyze.html",tweetanalysis="INVALID USERNAME")
             url="https://twitter.com/"+str(username)
             chrome_options = webdriver.ChromeOptions()
             chrome_options.add_argument("--headless")
             chrome_options.add_argument("--disable-gpu")
             browser = webdriver.Chrome(options=chrome_options)


             def tweetLocation(index):
                 return "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div/div["+str(index)+"]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div/div/span"
             try:
                browser.get(url)
                time.sleep(1.5)



                currentHeight=0

                tweetstring=""
                #HERE WE TAKE ACCOUNT İNFOS:
                time.sleep(0.2)
                try:
                    name="name: "+browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/span").text
                    username="username: "+browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/span").text
                except:
                     browser.close()
                     return render_template("tweetanalyze.html",tweetanalysis1=" INVALID USERNAME!",name="SOMETHİNG HAPPENED",username="INVALID USERNAME!")



                count_char=0

                for i in range(30):


                    try:
                        x = browser.find_element_by_xpath(tweetLocation(i + 1))
                        time.sleep(0.07)
                        tweetstring+=x.text+" "
                        count_char+=len(x.text)+1
                        if count_char>3500:
                            print("************************************************************************************")
                            print("OVERLOADED")
                            print("************************************************************************************")
                            browser.close()
                            return render_template("main.html",tweetanalysis1="TWEETS OVERLOADED! ",name=name,username="TWEETS OVERLOADED!")


                        browser.execute_script("window.scrollTo("+str(currentHeight)+","+str(currentHeight+300)+")")
                        currentHeight+=300
                        time.sleep(0.07)
                    except:
                        time.sleep(0.05)
                        continue



                browser.close()
                if len(tweetstring)<15:

                     print("************************************************************************************")
                     print("not enough tweets")
                     print("************************************************************************************")
                     return render_template("tweetanalyze.html",tweetanalysis1=" TWEETS ARE NOT ENOUGH!",name=name,username="TWEETS ARE NOT ENOUGH!")


                tweetstring=GoogleTranslator(source="auto",target="en").translate(tweetstring)
                #burada  apiye istek yolluyoruz


                url = "https://japerk-text-processing.p.rapidapi.com/sentiment/"
                text=tweetstring
                if text== "":
                    text="neutral"
                payload = "text="+text+"&language=english"
                headers = {
                    'content-type': "application/x-www-form-urlencoded",
                    'x-rapidapi-host': "",
                    'x-rapidapi-key': ""
                    }

                response = requests.request("POST", url, data=payload.encode("utf-8"), headers=headers)

                dicti=json.loads(response.text)
                label=dicti["label"]
                if label == "pos":
                    label="POSITIVE"
                    polarityRate=dicti["probability"]["pos"]
                    polarityRate=math.floor(polarityRate*100)
                elif label == "neg":
                    label="NEGATIVE"
                    polarityRate = dicti["probability"]["neg"]
                    polarityRate = math.floor(polarityRate * 100)
                else:
                    label="NEUTRAL"
                    polarityRate = dicti["probability"]["neutral"]
                    polarityRate = math.floor(polarityRate * 100)

                sent_text="Dominance: "+str(label) +" %"+str(polarityRate)

                return render_template("tweetanalyze.html", tweetanalysis1=sent_text,name=name,username=username)


             except:
                 browser.close()
                 return render_template("tweetanalyze.html",tweetanalysis1="INVALID USERNAME! ",name="SOMETHİNG HAPPENED",username="INVALID USERNAME!")



    else:

        return render_template("tweetanalyze.html",timewarning="THİS COULD TAKE A FEW SECONDS..")





@app.route("/", methods=['POST', 'GET'])
def anaSayfa():
    if request.method=="POST":
        if "text" in request.form:

            text=request.form["text"]

            if type(text)!= str:
                return render_template("tweetanalyze.html",textanalysis1="Text must contain characters, not just numbers.")
            else:
                try:

                    text=GoogleTranslator(source="auto",target="en").translate(text)

                    #burada apiye istek yolluyoruz

                    url = "https://japerk-text-processing.p.rapidapi.com/sentiment/"
                    text=text
                    if text== "":
                        text="neutral"
                    payload = "text="+text+"&language=english"
                    headers = {
                        'content-type': "application/x-www-form-urlencoded",
                        'x-rapidapi-host': "",
                        'x-rapidapi-key': ""
                        }

                    response = requests.request("POST", url, data=payload.encode("utf-8"), headers=headers)
                    print(response.text)
                    dicti=json.loads(response.text)
                    label=dicti["label"]
                    if label == "pos":
                        label="POSITIVE"
                        polarityRate=dicti["probability"]["pos"]
                        polarityRate=math.floor(polarityRate*100)
                    elif label == "neg":
                        label="NEGATIVE"
                        polarityRate = dicti["probability"]["neg"]
                        polarityRate = math.floor(polarityRate * 100)
                    else:
                        label="NEUTRAL"
                        polarityRate = dicti["probability"]["neutral"]
                        polarityRate = math.floor(polarityRate * 100)

                    sent_text="Dominance: "+str(label) +" %"+str(polarityRate)




                    return render_template("main.html",textanalysis1=sent_text)
                except:
                    return render_template("main.html",textanalysis1="SOMETHİNG HAPPENED, TRY AGAİN.")
    else:

        return render_template("main.html")



if __name__ == "__main__":
    app.run(debug=True)