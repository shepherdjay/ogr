# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

import pytest
from gitlab import GitlabGetError
from requre.online_replacing import record_requests_for_all_methods

from tests.integration.gitlab.base import GitlabTests

from ogr import GitlabService
from ogr.exceptions import GitlabAPIException
from ogr.services.gitlab.pull_request import GitlabPullRequest


@record_requests_for_all_methods()
class Service(GitlabTests):
    def test_project_create(self):
        """
        Remove https://gitlab.com/$USERNAME/new-ogr-testing-repo before data regeneration
        """
        name_of_the_repo = "new-ogr-testing-repo"
        project = self.service.get_project(
            repo=name_of_the_repo, namespace=self.service.user.get_username()
        )
        with pytest.raises(GitlabGetError):
            assert project.gitlab_repo

        new_project = self.service.project_create(name_of_the_repo)
        assert new_project.repo == name_of_the_repo
        assert new_project.gitlab_repo

        project = self.service.get_project(
            repo=name_of_the_repo, namespace=self.service.user.get_username()
        )
        assert project.gitlab_repo

    def test_project_create_with_description(self):
        """
        Remove the following project before data regeneration:
        https://gitlab.com/$USERNAME/new-ogr-testing-repo-with-description
        """
        name_of_the_repo = "new-ogr-testing-repo-with-description"
        description = "The description of the newly created project."

        project = self.service.get_project(
            repo=name_of_the_repo,
            namespace=self.service.user.get_username(),
        )
        with pytest.raises(GitlabGetError):
            assert project.gitlab_repo

        new_project = self.service.project_create(
            name_of_the_repo,
            description=description,
        )
        assert new_project.repo == name_of_the_repo
        assert new_project.gitlab_repo
        assert new_project.get_description() == description

        project = self.service.get_project(
            repo=name_of_the_repo, namespace=self.service.user.get_username()
        )
        assert project.gitlab_repo
        assert project.get_description() == description

    def test_project_create_in_the_group(self):
        """
        Remove https://gitlab.com/packit-service/new-ogr-testing-repo-in-the-group
        before data regeneration.
        """
        name_of_the_repo = "new-ogr-testing-repo-in-the-group"
        namespace_of_the_repo = "packit-service"
        project = self.service.get_project(
            repo=name_of_the_repo, namespace=namespace_of_the_repo
        )
        with pytest.raises(GitlabGetError):
            assert project.gitlab_repo

        new_project = self.service.project_create(
            repo=name_of_the_repo, namespace=namespace_of_the_repo
        )
        assert new_project.repo == name_of_the_repo
        assert new_project.namespace == namespace_of_the_repo
        assert new_project.gitlab_repo

        project = self.service.get_project(
            repo=name_of_the_repo, namespace=namespace_of_the_repo
        )
        assert project.gitlab_repo

    def test_project_create_duplicate(self):
        """
        Remove https://gitlab.com/$USERNAME/new-ogr-testing-repo-fail before data regeneration
        """
        name_of_the_repo = "new-ogr-testing-repo-fail"
        project = self.service.get_project(
            repo=name_of_the_repo, namespace=self.service.user.get_username()
        )
        with pytest.raises(GitlabGetError):
            assert project.gitlab_repo

        self.service.project_create(name_of_the_repo)
        with pytest.raises(GitlabAPIException):
            self.service.project_create(name_of_the_repo)

    def test_service_without_auth(self):
        service = GitlabService()
        assert service.gitlab_instance
        assert service.get_project(namespace="gnachman", repo="iterm2").exists()

    def test_list_projects_with_namespace_input(self):
        name_of_the_repo = "inkscape"
        number_of_projects = 10
        projects = self.service.list_projects(namespace=name_of_the_repo)
        assert len(projects) == number_of_projects

    def test_list_projects_with_namespace_input_and_language_input(self):
        name_of_the_repo = "inkscape"
        language = "C++"
        number_of_projects = 2
        projects = self.service.list_projects(
            namespace=name_of_the_repo, language=language
        )
        assert len(projects) == number_of_projects

    def test_wrong_auth(self):
        with pytest.raises(GitlabAPIException):
            self.service.project_create("test")

    def test_wrong_auth_static_method(self):
        # Verify that the exception handler is applied to static methods
        with pytest.raises(GitlabAPIException):
            GitlabPullRequest.get(self.project, 1)
