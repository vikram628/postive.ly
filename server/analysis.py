from datetime import datetime
import time
import matplotlib.pyplot as plt
import random
import io
import threading


def filter24hours(data):

    now = datetime.timestamp(datetime.now())
    return sorted([d for d in data if (now - d["timestamp"]) < 86400], key=lambda x: x["timestamp"])


def filter30days(data):

    now = datetime.timestamp(datetime.now())
    return sorted([d for d in data if (now - d["timestamp"]) < (86400 * 30)], key=lambda x: x["timestamp"])


def messageStats(data):

    pos = [d for d in data if d["score"] > 0.5]
    neg = [d for d in data if d["score"] <= 0.5]
    avg = sum([d["score"] for d in data]) / len(data)
    top5 = [d["message"] for d in sorted(data, key=lambda x: -x["score"])[:min(5, len(data))]]

    return {
        "num_pos": len(pos),
        "num_neg": len(neg),
        "avg_score": avg,
        "top_5": top5
    }


def graph24hours(data, stats):

    X = [d["timestamp"] for d in data[4:]]
    Y = [sum([d["score"] for d in data[:i]])/i for i in range(5, len(data)+1)]

    """
    totalScore = 0
    numberPoints = 0
    for message in data:
        totalScore += message["score"]
        numberPoints += 1
        average = totalScore/numberPoints
        Y.append(average)
    """

    plt.plot(X, Y, color="skyblue", linewidth=4, alpha=0.3)
    plt.xticks([])
    plt.xlabel("Your Day")
    plt.ylabel("Average Mood Score")


def graphRatio(data, stats):

    labels = ["Positive Thoughts", "Negative Thoughts"]
    colors = ["lemonchiffon", "lightcyan"]
    explode = (0.05, 0)
    plt.pie([stats["num_pos"], stats["num_neg"]], colors=colors, explode=explode, labels=labels, autopct="%1.0f%%")


def graph30days(data, stats):

    data = [random.random() for i in range(30)]
    plt.hist(data, [0, 0.2, 0.4, 0.6, 0.8, 1.0], rwidth=0.8, color="lemonchiffon")
    plt.xticks([])
    plt.xlabel("Mood Score Distribution")
    plt.ylabel("Number of Days")


graph_mutex = threading.Lock()
def generateGraph(graph, data, stats, small=True):

    graph_mutex.acquire()

    if small:
        fig = plt.figure(figsize=(10, 10))
    else:
        fig = plt.figure(figsize=(20, 10))

    graph(data, stats)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    plt.close(fig)

    graph_mutex.release()
    return buf
