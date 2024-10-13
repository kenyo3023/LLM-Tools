from github import GithubException


class GithubContentTraverser:

    def get_metadata(content):
        metadata = content._rawData
        return metadata

    @classmethod
    def traverse(cls, repo, path:str="", cur_depth:int=0, max_depth:int=10):
        file_names = []

        if cur_depth >= max_depth:
            return file_names

        contents = repo.get_contents(path)
        if not isinstance(contents, list):
            contents = [contents]

        for content in contents:
            if content.type == "dir":
                file_names.extend(cls.traverse(repo, content.path, cur_depth+1, max_depth))
            else:
                # file_names.append(content)
                file_names.append(cls.get_metadata(content))

        return file_names


class GithubAPITOOL:

    def __init__(self, client):
        self.client = client

    def get_repo(
        self,
        full_name_or_id: int | str,
        get_stargazers_count:bool = True,
        # get_issues:bool = True,
        get_contents:str | None = "",
        get_branch:str | None = None,
        get_commits:str | None = None,
    ):
        repo = self.client.get_repo(full_name_or_id=full_name_or_id)

        metadata = {}
        if get_stargazers_count:
            metadata['stargazers_count'] = repo.stargazers_count

        # if get_issues:
        #     issues = repo.get_issues(state='all')[:10]
        #     issues = [filter_attrs(issue, pattern='all') for issue in issues]
        #     metadata['issues'] = issues

        if isinstance(get_contents, str):
            path = get_contents
            contents = GithubContentTraverser.traverse(repo, path, max_depth=3)
            metadata['contents'] = contents

        if isinstance(get_branch, str):
            branch_name = get_branch
            try:
                branch_meta = repo.get_branch(branch_name)._rawData
            except GithubException as e:
                branch_meta = e._GithubException__data
            except:
                branch_meta = {
                    'message': 'Unknown',
                    'documentation_url': 'https://docs.github.com/rest/branches/branches#get-a-branch',
                    'status': '503'
                }
            metadata['branch'] = branch_meta

        if isinstance(get_commits, str):
            sha = get_commits
            commits = [commit_meta._rawData for commit_meta in repo.get_commits(sha)[:10]]
            metadata['commits'] = commits

        return metadata