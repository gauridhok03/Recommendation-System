from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# =========================================================
# PUT YOUR GEMINI API KEY HERE
# =========================================================

API_KEY = "AQ.Ow"

# Gemini model
MODEL = "gemini-3.5-flash"


# =========================================================
# MOVIE DATA
# =========================================================

movies = {
    "action": [
        ["John Wick", 8.5],
        ["The Dark Knight", 9.0],
        ["Mission Impossible", 8.2],
        ["Mad Max: Fury Road", 8.1],
        ["Gladiator", 8.5],
        ["Top Gun: Maverick", 8.3]
    ],

    "sci-fi": [
        ["Interstellar", 8.9],
        ["Inception", 8.8],
        ["The Matrix", 8.7],
        ["Avatar", 7.9],
        ["The Martian", 8.0],
        ["Dune", 8.2]
    ],

    "comedy": [
        ["3 Idiots", 8.4],
        ["Free Guy", 7.8],
        ["Jumanji", 7.5],
        ["The Hangover", 7.7],
        ["Deadpool", 8.0],
        ["Central Intelligence", 6.9]
    ],

    "romance": [
        ["Titanic", 7.9],
        ["The Notebook", 7.8],
        ["La La Land", 8.0],
        ["Me Before You", 7.4],
        ["A Walk to Remember", 7.3],
        ["The Fault in Our Stars", 7.7]
    ],

    "horror": [
        ["The Conjuring", 7.5],
        ["Insidious", 6.8],
        ["It", 7.3],
        ["Annabelle", 5.9],
        ["The Nun", 5.3],
        ["Smile", 6.5]
    ]
}


# =========================================================
# BOOK DATA
# =========================================================

books = {
    "fiction": [
        ["The Alchemist", 4.7],
        ["To Kill a Mockingbird", 4.8],
        ["The Great Gatsby", 4.5],
        ["The Kite Runner", 4.8],
        ["The Book Thief", 4.7],
        ["1984", 4.8]
    ],

    "fantasy": [
        ["Harry Potter", 4.9],
        ["The Hobbit", 4.8],
        ["The Lord of the Rings", 4.9],
        ["Percy Jackson", 4.7],
        ["The Chronicles of Narnia", 4.6],
        ["Eragon", 4.5]
    ],

    "self-help": [
        ["Atomic Habits", 4.8],
        ["The Power of Now", 4.6],
        ["Think and Grow Rich", 4.7],
        ["Deep Work", 4.7],
        ["The 7 Habits of Highly Effective People", 4.8],
        ["Ikigai", 4.6]
    ],

    "finance": [
        ["Rich Dad Poor Dad", 4.7],
        ["The Psychology of Money", 4.8],
        ["The Intelligent Investor", 4.7],
        ["Money Master the Game", 4.5],
        ["Think and Grow Rich", 4.7],
        ["Your Money or Your Life", 4.4]
    ],

    "mystery": [
        ["Sherlock Holmes", 4.8],
        ["The Da Vinci Code", 4.6],
        ["Gone Girl", 4.5],
        ["Murder on the Orient Express", 4.7],
        ["The Silent Patient", 4.6],
        ["And Then There Were None", 4.8]
    ]
}


# =========================================================
# HTML + CSS + JAVASCRIPT
# =========================================================

HTML = """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Media Recommendation Chatbot</title>


<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

body {
    background: #f1f3f6;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.chat-container {
    width: 420px;
    height: 650px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}


/* Header */

.chat-header {
    background: linear-gradient(135deg, #6c5ce7, #4834d4);
    color: white;
    padding: 20px;
    text-align: center;
}

.chat-header h2 {
    margin-bottom: 5px;
}

.chat-header p {
    font-size: 13px;
    opacity: 0.9;
}


/* Chat */

.chat-box {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: #f8f9fb;
}

.message {
    max-width: 85%;
    padding: 12px 15px;
    margin-bottom: 12px;
    border-radius: 15px;
    line-height: 1.5;
    font-size: 14px;
}

.bot {
    background: #e8e7ff;
    color: #222;
    border-bottom-left-radius: 4px;
}

.user {
    background: #6c5ce7;
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 4px;
}


/* Buttons */

.options {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.option-btn {
    border: none;
    background: white;
    color: #6c5ce7;
    border: 1px solid #6c5ce7;
    padding: 9px 13px;
    border-radius: 20px;
    cursor: pointer;
    transition: 0.2s;
}

.option-btn:hover {
    background: #6c5ce7;
    color: white;
}


/* Input */

.input-area {
    display: flex;
    padding: 12px;
    border-top: 1px solid #ddd;
    background: white;
}

.input-area input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 25px;
    outline: none;
}

.send-btn {
    margin-left: 8px;
    width: 45px;
    border: none;
    border-radius: 50%;
    background: #6c5ce7;
    color: white;
    cursor: pointer;
    font-size: 18px;
}

.send-btn:hover {
    background: #4834d4;
}


/* Recommendation */

.recommendation {
    background: white;
    padding: 10px;
    margin-top: 8px;
    border-radius: 10px;
    border-left: 4px solid #6c5ce7;
}

.recommendation strong {
    color: #333;
}

.rating {
    color: #f39c12;
    font-size: 13px;
}

</style>

</head>


<body>


<div class="chat-container">


<div class="chat-header">

<h2>Recommendation System</h2>

<p>Movies & Books Recommendation System</p>

</div>


<div class="chat-box" id="chatBox">


<div class="message bot">

👋 Hello! Welcome to MediaBot.

<br><br>

What would you like recommendations for?


<div class="options">

<button
class="option-btn"
onclick="selectType('movie')">

🎬 Movies

</button>


<button
class="option-btn"
onclick="selectType('book')">

📚 Books

</button>

</div>

</div>

</div>


<div class="input-area">

<input
type="text"
id="userInput"
placeholder="Type your choice..."
onkeydown="handleEnter(event)"
>

<button
class="send-btn"
onclick="sendMessage()">

➤

</button>

</div>


</div>


<script>

let selectedType = "";


/* =====================================================
   ADD MESSAGE
===================================================== */

function addMessage(message, sender) {

    const chatBox =
        document.getElementById("chatBox");

    const div =
        document.createElement("div");

    div.classList.add("message", sender);

    div.innerHTML = message;

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


/* =====================================================
   SELECT MOVIE OR BOOK
===================================================== */

function selectType(type) {

    selectedType = type;

    if (type === "movie") {

        addMessage("🎬 Movies", "user");

        setTimeout(function() {

            addMessage(
                "Great choice! Tell me what kind of movie you want. You can describe it in your own words.",
                "bot"
            );

        }, 300);

    } else {

        addMessage("📚 Books", "user");

        setTimeout(function() {

            addMessage(
                "Great choice! Tell me what kind of book you want. You can describe it in your own words.",
                "bot"
            );

        }, 300);
    }
}


/* =====================================================
   SEND MESSAGE
===================================================== */

function sendMessage() {

    const input =
        document.getElementById("userInput");

    const message =
        input.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");

    input.value = "";


    /* User selects movie */

    if (
        message.toLowerCase() === "movie" ||
        message.toLowerCase() === "movies"
    ) {

        selectType("movie");
        return;
    }


    /* User selects book */

    if (
        message.toLowerCase() === "book" ||
        message.toLowerCase() === "books"
    ) {

        selectType("book");
        return;
    }


    /* Must select movie/book first */

    if (selectedType === "") {

        addMessage(
            "Please select 🎬 Movies or 📚 Books first.",
            "bot"
        );

        return;
    }


    addMessage(
        "🤖 Gemini AI is analyzing your preference...",
        "bot"
    );


    /* Send request to Python */

    fetch("/recommend", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            message: message,

            type: selectedType

        })

    })

    .then(function(response) {

        return response.json();

    })

    .then(function(data) {

        if (data.error) {

            addMessage(
                "❌ " + data.error,
                "bot"
            );

            return;
        }

        displayRecommendation(data.response);

    })

    .catch(function(error) {

        console.log(error);

        addMessage(
            "❌ Could not connect to the Python server.",
            "bot"
        );

    });
}


/* =====================================================
   DISPLAY AI RESPONSE
===================================================== */

function displayRecommendation(text) {

    let html =
        "🤖 <b>AI Recommendations</b><br><br>";

    const lines = text.split("\\n");

    let title = "";
    let rating = "";
    let reason = "";


    lines.forEach(function(line) {

        line = line.trim();

        if (line === "") {
            return;
        }


        /* Genre */

        if (line.startsWith("GENRE:")) {

            const genre =
                line.replace("GENRE:", "").trim();

            html +=
                "<b>🎯 Genre: " +
                genre +
                "</b><br><br>";
        }


        /* Recommendation */

        else if (
            line.startsWith("RECOMMENDATION")
        ) {

            if (title !== "") {

                html +=
                    '<div class="recommendation">' +
                    '<strong>' + title + '</strong>' +
                    '<br>' +
                    '<span class="rating">⭐ ' +
                    rating +
                    '</span>' +
                    '<br>' +
                    '💡 ' + reason +
                    '</div>';
            }

            title = "";
            rating = "";
            reason = "";
        }


        /* Title */

        else if (line.startsWith("TITLE:")) {

            title =
                line.replace("TITLE:", "").trim();
        }


        /* Rating */

        else if (line.startsWith("RATING:")) {

            rating =
                line.replace("RATING:", "").trim();
        }


        /* Reason */

        else if (line.startsWith("REASON:")) {

            reason =
                line.replace("REASON:", "").trim();
        }

    });


    /* Add final recommendation */

    if (title !== "") {

        html +=
            '<div class="recommendation">' +
            '<strong>' + title + '</strong>' +
            '<br>' +
            '<span class="rating">⭐ ' +
            rating +
            '</span>' +
            '<br>' +
            '💡 ' + reason +
            '</div>';
    }


    addMessage(html, "bot");
}


/* =====================================================
   ENTER KEY
===================================================== */

function handleEnter(event) {

    if (event.key === "Enter") {

        sendMessage();

    }
}

</script>


</body>

</html>
"""


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template_string(HTML)


# =========================================================
# GEMINI API
# =========================================================

@app.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        user_message = data.get("message", "")
        media_type = data.get("type", "movie")


        if not user_message:

            return jsonify({
                "error": "Please enter your preference."
            })


        # Choose movie or book dataset

        if media_type == "movie":

            dataset = movies

        else:

            dataset = books


        # Create list for AI

        available_content = ""


        for genre, items in dataset.items():

            available_content += "\nGENRE: " + genre + "\n"

            for title, rating in items:

                available_content += (
                    "TITLE: " + title +
                    " | RATING: " + str(rating) +
                    "\n"
                )


        # =====================================================
        # AI PROMPT
        # =====================================================

        prompt = f"""
You are an AI recommendation assistant.

The user wants {media_type} recommendations.

User preference:
{user_message}

Available {media_type}:

{available_content}

Understand the user's natural-language preference.

Choose the most suitable genre.

Then recommend exactly 3 items from the available list.

Use ratings as an additional factor.

DO NOT invent any titles.

Only use titles from the available list.

Give a short reason for each recommendation.

Return exactly this format:

GENRE: genre

RECOMMENDATION 1:
TITLE: title
RATING: rating
REASON: reason

RECOMMENDATION 2:
TITLE: title
RATING: rating
REASON: reason

RECOMMENDATION 3:
TITLE: title
RATING: rating
REASON: reason
"""


        # =====================================================
        # GEMINI REQUEST
        # =====================================================

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/"
            + MODEL +
            ":generateContent?key=" +
            API_KEY
        )


        payload = {

            "contents": [

                {
                    "parts": [

                        {
                            "text": prompt
                        }

                    ]
                }

            ]

        }


        response = requests.post(
            url,
            json=payload,
            timeout=60
        )


        # =====================================================
        # CHECK GEMINI RESPONSE
        # =====================================================

        if response.status_code != 200:

            print("Gemini status:", response.status_code)
            print("Gemini response:", response.text)

            try:

                error_data = response.json()

                error_message = (
                    error_data
                    .get("error", {})
                    .get("message", response.text)
                )

            except:

                error_message = response.text


            return jsonify({
                "error":
                "Gemini API Error: " +
                error_message
            }), 500


        result = response.json()


        # Get generated text

        ai_text = (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        )


        return jsonify({
            "response": ai_text
        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print("======================================")
    print(" Media Recommendation AI")
    print("======================================")
    print("")
    print("Open this in Chrome:")
    print("http://127.0.0.1:5000")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )