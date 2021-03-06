# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""This module implements the abstract base class for backend modules.

To create add-on backend modules subclass the Backend class in this module.
Doing so requires that the required backend interface is implemented.
"""
from abc import ABC, abstractmethod

import qiskit
from .models import BackendStatus


class BaseBackend(ABC):
    """Base class for backends."""

    @abstractmethod
    def __init__(self, configuration, provider=None):
        """Base class for backends.

        This method should initialize the module and its configuration, and
        raise an exception if a component of the module is
        not available.

        Args:
            configuration (dict): configuration dictionary
            provider (BaseProvider): provider responsible for this backend

        Raises:
            FileNotFoundError if backend executable is not available.
            QISKitError: if there is no name in the configuration
        """
        if 'name' not in configuration:
            raise qiskit.QISKitError('backend does not have a name.')
        self._configuration = configuration
        self._provider = provider

    @abstractmethod
    def run(self, qobj):
        """Run a Qobj on the the backend."""
        pass

    def configuration(self):
        """Return backend configuration"""
        return self._configuration

    def properties(self):
        """Return backend properties"""
        return {}

    def provider(self):
        """Return the backend Provider.

        Returns:
            BaseProvider: the Provider responsible for this backend.
        """
        return self._provider

    def status(self):
        """Return backend status.

        Returns:
            BackendStatus: the status of the backend.
        """
        return BackendStatus(backend_name=self.name(),
                             backend_version=qiskit.__version__,
                             operational=True,
                             pending_jobs=0,
                             status_msg='')

    def name(self):
        """Return backend name"""
        return self._configuration['name']

    def __str__(self):
        return self.name()

    def __repr__(self):
        """Official string representation of a Backend.

        Note that, by Qiskit convention, it is consciously *not* a fully valid
        Python expression. Subclasses should provide 'a string of the form
        <...some useful description...>'. [0]

        [0] https://docs.python.org/3/reference/datamodel.html#object.__repr__
        """
        return "<{}('{}') from {}()>".format(self.__class__.__name__,
                                             self.name(),
                                             self._provider)
