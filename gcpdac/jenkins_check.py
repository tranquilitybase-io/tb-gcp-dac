##Import our dependencies
import jenkinsapi
import sys
from jenkinsapi.jenkins import Jenkins

JENKINS_ADMIN_USER = "admin"
JENKINS_PASSWORD = "gftdev@123"
JENKINS_URL = "http://34.89.36.243:8080/"


##Define a function to connect to Jenkins
# import config


def connectToJenkins():
    # server = Jenkins(config.JENKINS_URL)
    server = Jenkins(baseurl=JENKINS_URL, username=JENKINS_ADMIN_USER, password=JENKINS_PASSWORD)
    return server


##Define a function to give us all of our Jobs on our server
def getJenkinsJobs(server):
    # return server.get_jobs()
    # return server.jobs
    return server.keys()


##This next function has a LOT going on, so I'll comment as we go.
def runJenkinsJob(job, paramsMap):  ##Define a function to handle running our job
    if (len(job.get_params_list()) != len(sys.argv) - 3):  ##If we don't pass in enough arguments...
        print(
            "Error: Argument length mismatch. Please ensure that you're supplying enough arguments for the jenkins job.")
        exit()  ## ... exit the script.

    if (job.has_params()):  ## else, if that job has parameters
        builder = {}  ##we do some fancy magic to build our job.
        counter = 3  ##the first thing we want is arguement #3 from our command line
        for param in job.get_params_list():  # for each parameter the job has, set the command line arguement equal to it.
            builder[param] = sys.argv[counter]
            counter = counter + 1
        print("Starting job '" + job.name + "'.")  ##Let us know we're starting our job.
        job.invoke(None, False, False, 3, 15, builder, None, None)  ##Invoke the job from our wrapper library.

    else:
        job.invoke()  ##invoke the job with no parameters.


def blowup():  ##gives us some error output to help users the second time around.
    print("You need to specify a job name, task, and any arguements needed.")
    print("If you're trying to deploy jenkinsTestApp (version 2.0.0) to beta.")
    print("Try this: > Sinclair jenkinsTestApp deploy beta 2.0.0")
    exit()


def noJobs():
    print('Could not find the job that was entered.')


def get_server_instance():
    server = Jenkins(JENKINS_URL, username=JENKINS_ADMIN_USER, password=JENKINS_PASSWORD)
    return server


"""Get job details of each job that is running on the Jenkins instance"""


def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for job_name, job_instance in server.get_jobs():
        print('Job Name:%s' % (job_instance.name))
        print('Job Description:%s' % (job_instance.get_description()))
        print('Is Job running:%s' % (job_instance.is_running()))
        print('Is Job enabled:%s' % (job_instance.is_enabled()))


def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        print("Short Name:%s" % (plugin.shortName))
        print("Long Name:%s" % (plugin.longName))
        print("Version:%s" % (plugin.version))
        print("URL:%s" % (plugin.url))
        print("Active:%s" % (plugin.active))
        print("Enabled:%s" % (plugin.enabled))


def main():
    print(get_server_instance().version)
    get_job_details()
    get_plugin_details()


# def main():  ## Our main method is a little big, but it basically
#     # if (len(sys.argv) == 2):
#     #     blowup()
#     # else:
#     server = connectToJenkins()
#     server.get_credentials()
#     jobs = getJenkinsJobs(server)
#     for job in jobs:
#         print(type(job))
#         print(job)
#         # print(job.name)
#         # print(job.url)
#
#     # jobName = sys.argv[1] + " " + sys.argv[2]  ## builds our job name out of our first 2 arguments.
#     jobName = "Activator Deploy"
#     if (jobs.__contains__(jobName)):  ##make sure the job exists on the server.
#         job = server[jobName]  ##select the job
#         # args = {}
#         # runJenkinsJob(job, sys.argv)  ##run it
#         # runJenkinsJob(job, args)  ##run it
#         job.invoke()
#     else:
#         noJobs()
#

main()  ## run this fella
