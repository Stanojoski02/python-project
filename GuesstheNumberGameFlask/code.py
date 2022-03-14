from flask import Flask
import random
randomnumber = random.randint(1, 8)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1 style="color:red; text-align: center;">Choose a number !!</h1>'\
    '<p>select a number and type it in the search bar</p>' \
           '<img src="https://media1.giphy.com/media/L2wyMMZ9ZjDTyS6StQ/giphy.gif?cid=ecf05e47zwpzq3ox884w1dawiw9eiuz3ar3hv3cgi8l2sz8y&rid=giphy.gif&ct=g">'
@app.route("/<number>")
def guiz_game(number):
    if int(number) == randomnumber:
        return '<h1 style="color: red;"> !!!Finally hit!!! <h1>' \
               '<img src="https://media0.giphy.com/media/Mp5qadvO1bokZFzniy/giphy.gif?cid=ecf05e4755nej2ha29lqoelu52ameokddzke1zropn3epvz4&rid=giphy.gif&ct=g" width = 400>'
    else:
        if int(number)>randomnumber:
            a = "You are close but the number is smaller"
        else:
            a = "You are close but the number is bigger"
        if int(number)==1:
            return f"<h1>{a}</h1><img src='https://media3.giphy.com/media/l0ExncehJzexFpRHq/giphy.gif?cid=ecf05e47adw3gpxessx4lqavgs4hn5zgelnh9cax635e35za&rid=giphy.gif&ct=g'>"
        if int(number)==2:
            return f"<h1>{a}</h1><img src='https://media2.giphy.com/media/26gsqQxPQXHBiBEUU/giphy.gif?cid=ecf05e47fb0nz991q1u7aqbzulw0ckfv0us7sxj2po7xcuh9&rid=giphy.gif&ct=g'>"
        if int(number)==3:
            return f"<h1>{a}</h1><img src='https://media1.giphy.com/media/NRtZEyZjbLgr0BJ4B8/giphy.gif?cid=ecf05e478oiz05pntiw3c06hp1ygoi1zt4909irh8fu6nt2e&rid=giphy.gif&ct=g'>"
        if int(number)==4:
            return f'<h1>{a}</h1><img src="https://media0.giphy.com/media/d1E1szXDsHUs3WvK/giphy.gif?cid=ecf05e47wzwgj86ds3bcdlaczn8kfc1gjjzf2r8n0zay46ci&rid=giphy.gif&ct=g">'
        if int(number)==5:
            return f'<h1>{a}</h1><img src="https://media3.giphy.com/media/3oKIPuzqJQusn18UOk/giphy.gif?cid=ecf05e47n69sz6nvynl4h5s8wev5de8kqgw9k7gxiy43zcku&rid=giphy.gif&ct=g">'
        if int(number)==6:
            return f'<h1>{a}</h1><img src="https://media4.giphy.com/media/y4y2tPp5damibthJmy/giphy.gif?cid=ecf05e47g2t7hls4k3z114m3z5645fllsr65gob8j77mgjub&rid=giphy.gif&ct=g">'
        if int(number)==7:
            return f'<h1>{a}</h1><img src="https://media1.giphy.com/media/YGz18JiFxv8Zy/giphy.gif?cid=ecf05e47dbxuhz0e9h7mfb0gz6qx8fpnsa9afmv37v4u61om&rid=giphy.gif&ct=g">'
if __name__ == "__main__":
    app.run(debug=True)
