import html2text
import httplib2
from urlparse import urlparse, parse_qs
import re
from xml.dom.minidom import parseString
import json
from core.services.mail_services import notify_admin
from django.conf import settings
import socket
import urllib
import html2markdown

class IssueInfo(object):

    def __init__(self):
        self.error = ''
        self.project_name = ''
        self.issue_title = ''
        self.description = ''
        self.key = ''
        self.tracker = ''
        self.project_trackerURL = ''


def fetchIssueInfo(issueURL):
    if looks_like_github(issueURL):
        info = retriveGithubInfo(issueURL)
    elif looks_like_jira(issueURL):
        info = retriveJIRAInfo(issueURL)
    elif looks_like_bugzilla(issueURL):
        info = retriveBugzillaInfo(issueURL)
    elif looks_like_bitbucket(issueURL):
        info = retrieveBitBucketInfo(issueURL)
    elif looks_like_google_code(issueURL):
        info = retrieve_google_code_info(issueURL)
    elif looks_like_chromium(issueURL):
        info = retrieve_chromium_info(issueURL)
    elif looks_like_gitlab(issueURL):
        info = retrieveGitLabInfo(issueURL)
    else:
        info = IssueInfo()

    if info.error:
        print 'Error fetching info for: '+issueURL+' - '+info.error
        notify_admin('Error fetching info for: '+issueURL, info.error)
    return info


######## GITLAB ##########

def looks_like_gitlab(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'gitlab.com'

def retrieveGitLabInfo(url):
    parsedURL = urlparse(url)
    info = IssueInfo()
    pathTokens = parsedURL.path.split('/')  # [0] is empty, which is handled below
    # decode
    repo_owner_name = pathTokens[1]
    repo_name = pathTokens[2]
    dash = pathTokens[3]  # gitlab has a dash in the URL
    issues = pathTokens[4]
    issues_id = pathTokens[5]
    # check
    if len(pathTokens) < 6 or issues.lower() != 'issues':  # gitlab has added dash '-'
        info.error = "URL doesn't look like a GitLab issue link"
        return info
    info.key = issues_id
    info.tracker = 'GITLAB'
    info.project_name = repo_name
    info.project_trackerURL = parsedURL.scheme + '://' + '/'.join([parsedURL.netloc, repo_owner_name, repo_name, dash, issues])
    projectUrlEncode = urllib.quote(repo_owner_name) + "%2F" + urllib.quote(repo_name)
    issueJsonURL = parsedURL.scheme + '://' + parsedURL.netloc + '/api/v4/projects/' + projectUrlEncode + '/issues/' + info.key
    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)
    try:
        resp, content = h.request(issueJsonURL)
        if resp.status == 200:
            try:
                issueJson = json.loads(content)
                info.issue_title = issueJson['title']
                info.description = issueJson['description']
            except:
                info.error = 'Could not parse JSON view from: ' + issueJsonURL
        else:
            info.error = ('status %s: ' % resp.status) + issueJsonURL
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message
    return info

######## JIRA ##########

def retriveJIRAInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    last_after_slash = parsedURL.path.split('/')[-1]
    jira_key = last_after_slash
    path_before_jira_key = parsedURL.path.split('/'+jira_key)[0]
    project_abbrev = get_jira_project_abbrev(jira_key)
    xmlviewURL = parsedURL.scheme+'://'+parsedURL.netloc+get_jira_xml_view(parsedURL.path)
    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)
    try: 
        resp, content = h.request(xmlviewURL)
        info.key = jira_key
        info.tracker = 'JIRA'
        info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+path_before_jira_key+'/'+project_abbrev
        if(resp.status == 200):
            try:
                dom = parseString(content)
                info.project_name = dom.getElementsByTagName('project')[0].childNodes[0].wholeText
                info.issue_title = dom.getElementsByTagName('summary')[0].childNodes[0].wholeText
                info.description = ''
                if dom.getElementsByTagName('item')[0].getElementsByTagName('description')[0].childNodes:
                    info.description = html2markdown.convert(dom.getElementsByTagName('item')[0].getElementsByTagName('description')[0].childNodes[0].wholeText)


            except:
                info.error = 'Could not parse XML view from: '+xmlviewURL
        else:
            info.error = ('status %s: '%resp.status)+xmlviewURL
    except (httplib2.HttpLib2Error, socket.timeout, socket.error) as e:
        info.error = 'error: ' + e.message
    return info
            
    
def looks_like_jira(url):
    parsedURL = urlparse(url)
    path = parsedURL.path
    jira_key = path.split('/')[-1]
    if(path.endswith('/browse/'+jira_key)):
        match = re.match(r'[A-Z]+-\d+', jira_key)
        if(match):
            return match.group(0) == jira_key

def get_jira_project_abbrev(jira_key):
    match = re.match(r'[A-Z]+', jira_key)
    return match.group(0)

def get_jira_xml_view(path):
    jira_key = path.split('/')[-1]
    before_browse = path.split('browse/'+jira_key)[0]
    return before_browse+'/si/jira.issueviews%3aissue-xml/'+jira_key+'/'+jira_key+'.xml'

######## GITHUB ##########


def looks_like_github(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'github.com'


def retriveGithubInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 5 or pathTokens[3].lower() != 'issues':
        info.error = "URL doesn't look like a Github issue link"
        return info
    info.key = pathTokens[4]
    info.tracker = 'GITHUB'
    info.project_name = pathTokens[2]
    info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/'+pathTokens[1]+'/'+pathTokens[2]+'/'+pathTokens[3]
    auth = 'client_id=%s&client_secret=%s' % (settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET)
    issueJsonURL = 'https://api.github.com/repos' + parsedURL.path + '?' + auth
    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)
    try: 
        resp, content = h.request(issueJsonURL)
        if resp.status == 200:
            try:
                issueJson = json.loads(content)
                info.issue_title = issueJson['title']
                info.description = issueJson['body']
            except:
                info.error = 'Could not parse JSON view from: '+issueJsonURL
        else:
            info.error = ('status %s: '%resp.status)+issueJsonURL
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message
    return info


######### Bugzilla ########
# It still working in 2023-10-21
# TODO: info.description should not be info.issue_title . Try to parse original description.

def looks_like_bugzilla(url):
    parsedURL = urlparse(url)
    if parsedURL.path.lower().endswith('show_bug.cgi'):
        query = parsedURL.query.lower()
        match = re.match(r'id=\d+', query)
        if match:
            return match.group(0) == query
    return False


def retriveBugzillaInfo(url):
    parsedURL = urlparse(url)
    info = IssueInfo()
    info.error = ''
    info.key = parsedURL.query.split('id=')[1]
    info.tracker = 'BUGZILLA'
    pathBeforeShowBug=parsedURL.path.split('show_bug.cgi')[0]
    bugJsonURL = parsedURL.scheme+'://'+parsedURL.netloc+pathBeforeShowBug+'jsonrpc.cgi?method=Bug.get&params=[{"ids":['+info.key+']}]'
    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)
    try: 
        resp, content = h.request(bugJsonURL)
        if resp.status == 200:
            try:
                bugJson = json.loads(content)
                info.project_name = bugJson['result']['bugs'][0]['product']
                info.issue_title = bugJson['result']['bugs'][0]['summary']
                info.description = info.issue_title
                info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+pathBeforeShowBug+'buglist.cgi?product='+info.project_name
            except:
                info.error = 'Could not parse JSon view from: '+bugJsonURL
        elif resp.status == 404:
            pass
        return info
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message
        return info


########## BitBucket ########
# Bitbucket REST API version 1 REST API version 1 was permanently removed from the REST API.
# There is temporary support for limited 1.0 API resources.
# https://support.atlassian.com/bitbucket-cloud/docs/build-third-party-apps-with-bitbucket-cloud-rest-api/


def looks_like_bitbucket(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'bitbucket.org'


def retrieveBitBucketInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 5 or pathTokens[3].lower() != 'issue':
        info.error = "URL doesn't look like a BitBucket issue link"
        return info
    _username, _project_name, info.key = pathTokens[1], pathTokens[2], pathTokens[4]
    info.tracker = 'BITBUCKET'
    info.project_name = _project_name
    info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/'+_username+'/'+_project_name + '/issues'
    issueJsonURL = 'https://api.bitbucket.org/1.0/repositories/' + _username + '/' + _project_name + '/issues/' + pathTokens[4]
    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)
    try: 
        resp, content = h.request(issueJsonURL)
        if resp.status == 200:
            try:
                issueJson = json.loads(content)
                info.issue_title = issueJson['title']
                info.description = issueJson['content']
            except:
                info.error = 'Could not parse JSon view from: '+issueJsonURL
        else:
            info.error = ('status %s: '%resp.status)+issueJsonURL
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message
    return info


######## Google Code ##########
# Google Code itself is not working since 2016. Currently, they separate it in
# opensource.google.com, developers.google.com and code.google.com/archive

def looks_like_google_code(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'issuetracker.google.com'

def retrieve_google_code_info(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 3 or pathTokens[1] != 'issues':
        info.error = "URL doesn't look like a Google issue link"
        return info
    info.key = pathTokens[2]
    info.tracker = 'GOOGLECODE'
    info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/issues'

    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)

    req_headers = {
        'Accept': 'application/json',
    }

    component_id = ''
    try:
        # get issue title and description
        issue_api_url = 'https://issuetracker.google.com/action/issues/' + info.key + '/events?currentTrackerId='
        resp, content = h.request(issue_api_url, headers=req_headers)
        if resp.status == 200:
            try:
                # json extract: ... "b.IssueComment", null, null, ..., null, [ "<--- DESCRIPTION --->" ] ...
                info.description = content.split('IssueComment"')[1].split('"')[1]  # first comment == issue description
                # json extract: ... "Title", 1, [ ... ], false, [ null, [ null, "<--- TITLE --->" ], ], ] ...
                info.issue_title = content.split('Title"')[1].split('"')[1]  # search for next quote `"` after `"Title"`
                # json extract: ... "Component", 1, [ ... ], false, [ null, [ null, "<--- TITLE --->" ], ], ] ...
                component_id = content.split('Component"')[1].split('"')[1]  # search for next quote `"` after `"Component"`
            except:
                info.error = 'Could not parse json from: '+issue_api_url
        else:
            info.error = ('status %s: '%resp.status) + ('response %s: '%content) + issue_api_url
        if component_id is not '':
            # get project name (component hierarchy)
            component_api_url = 'https://issuetracker.google.com/action/components/' + component_id
            resp, content = h.request(component_api_url, headers=req_headers)
            if resp.status == 200:
                try:
                    # json extract: ... "b.Component", ... [ "<--- COMPONENT --->", ..., [ "<- FULL ->", "<- COMPONENT ->", "<- PATH ->", ... ] ...
                    rest = '"'.join(content.split('b.Component"')[1].split('"')[3:])  # == "<- FULL ->", "<- COMPONENT ->", "<- PATH ->", ... ] ...
                    component_list = rest.split(']')[0].replace('"', '').split(',')  # trim list end, remove quotes, split on commas
                    info.project_name = ' > '.join([c.strip() for c in component_list])
                except:
                    info.error = 'Could not parse json from: '+component_api_url
            else:
                info.error = ('status %s: '%resp.status) + ('response %s: '%content) + component_api_url
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message
    return info

###### CHROMIUM ######
def looks_like_chromium(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'bugs.chromium.org'

def retrieve_chromium_info(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 5 or pathTokens[1] != 'p' or pathTokens[3] != 'issues' or pathTokens[4] != 'detail':
        info.error = "URL doesn't look like a Chromium issue link"
        return info
    info.key = parse_qs(parsedURL.query)['id'][0]
    info.tracker = 'CHROMIUM'
    info.project_name = pathTokens[2]
    info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/p/'+info.project_name+'/issues/list'
    issue_title_url = 'https://bugs.chromium.org/prpc/monorail.Issues/GetIssue'
    issue_comments_url = 'https://bugs.chromium.org/prpc/monorail.Issues/ListComments'

    h = httplib2.Http(disable_ssl_certificate_validation=True, timeout=settings.FETCH_ISSUE_TIMEOUT)

    # get xsrf token (needed because: https://groups.google.com/a/chromium.org/g/infra-dev/c/8eiyZbsHc_4/m/HfIXUkkuBAAJ)
    try:
        resp, content = h.request(url)
        if resp.status == 200:
            try:
                # html extract: ... <head> ... <script ...> ... window.CS_env = { ..., 'token': '<---- XSRF TOKEN ---->', ...
                xsrf_token = content.split("token'")[1].split("'")[1]
            except:
                info.error = 'Could not parse HTML from: '+url
        else:
            info.error = ('status %s: '%resp.status)+url
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message

    req_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Xsrf-Token': xsrf_token
    }
    req_body = '{ "issueRef": { "localId": ' + info.key +  ', "projectName": "' + info.project_name + '" } }'

    try:
        # get issue title
        resp, content = h.request(issue_title_url, method='POST', headers=req_headers, body=req_body)
        if resp.status == 200:
            try:
                content_json = json.loads(content[4:])  # skip `)]}'` at beginning
                info.issue_title = content_json['issue']['summary']
            except:
                info.error = 'Could not parse json from: '+issue_title_url
        else:
            info.error = ('status %s: '%resp.status) + ('response %s: '%content) + issue_title_url
        # get issue comments
        resp, content = h.request(issue_comments_url, method='POST', headers=req_headers, body=req_body)
        if resp.status == 200:
            try:
                content_json = json.loads(content[4:])  # skip `)]}'` at beginning
                info.description = content_json['comments'][0]['content']  # first comment == issue description
                print(info.description)
            except:
                info.error = 'Could not parse json from: '+issue_comments_url
        else:
            info.error = ('status %s: '%resp.status) + ('response %s: '%content) + issue_comments_url
    except (httplib2.HttpLib2Error, socket.timeout) as e:
        info.error = e.message
    return info


