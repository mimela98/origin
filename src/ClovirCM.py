import git
import pymysql
import shutil
import tensorflow as tf

from os import environ

from git.exc import GitCommandError

def push(path):
        repo = createOrGetRepository(path)
        try:
                repo.git.add('*')
                repo.git.commit("-m model update")

        except GitCommandError as e:
                print(e)
                pass

        repo.git.push("origin", "master")

def pull(path):
        repo = createOrGetRepository(path)
        origin = repo.remote()
        origin.fetch()
        origin.pull()

def createOrGetRepository(path):
        git.Repo.init(path)
        repo = git.Repo(path)
        try:
                git.Remote.add(repo, "origin", getEnv("GIT_URL"))

        except GitCommandError as e:
                print(e)
                pass

        return repo

def query(query, needReturn, needCommit):
        try:
                conn = getConnection(getEnv("DB_HOST"), getEnv("DB_USER_ID"), getEnv("DB_PASSWORD"), getEnv("DB_NAME"))
                cur = conn.cursor()
                cur.execute(query)
                if(needReturn):
                        row = cur.fetchall()
                if(needCommit):
                        conn.commit()
        except Exception as e:
                print(e)
        finally:
                conn.close()
        if(needReturn):
                return row

def getConnection(host, user, pw, db):
        return pymysql.connect(host=host, user=user, password=pw, db=db, charset="utf8")

def simple_save(sess, inputs, outputs):
        path = getEnv("GIT_REPO_PATH")
        l = list(inputs.keys())
        try:
            shutil.rmtree(path + '/model/' + getEnv("APP_VER"))
        except OSError:
            pass
        tf.saved_model.simple_save(sess, path + "/model/" + getEnv("APP_VER"), inputs=inputs, outputs=outputs)
        updateOrinsert(l)
        push(path)

def getEnv(name):
        return environ[name]

def updateOrinsert(param) :
        try:
                query("""
                    INSERT INTO cm_ai_model(
                        APP_ID, 
                        `INPUT`, 
                        UPD_TMS
                    ) VALUES(
                        '""" + getEnv("PRJ_ID") + """', 
                        '[""" + ",".join(param) + """]', 
                        CURRENT_TIMESTAMP
                    );
                """, False, True)
        except BaseException:
                query("""
                    UPDATE cm_ai_model SET 
                        `INPUT`='[""" + ",".join(param) + """]',
                        UPD_TMS=CURRENT_TIMESTAMP
                    WHERE APP_ID='""" + getEnv("PRJ_ID") + """';
                """, False, True)
                pass
