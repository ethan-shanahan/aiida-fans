"""Custom Data Plugins for AiiDA-FANS."""

from aiida.orm import RemoteData


class MicrostructureData(RemoteData):
    """A node representing a specific microstructure dataset within a remote HDF5 file.

    Remember to pass a computer!
    """

    def __init__(self, file_path: str | None = None, dataset_name: str | None = None, **kwargs):
        """Construct a new instance then set the file path and dataset name.

        Args:
            file_path (str | None, optional): an absolute file path. Defaults to None.
            dataset_name (str | None, optional): the name of a group within the file. Defaults to None.
            **computer (Computer | None, optional): the computer where the file is located. Defaults to None.
        """
        super().__init__(remote_path=file_path, **kwargs)
        self.base.attributes.set("dataset_name", dataset_name)

    @property
    def dataset_name(self):
        """Return the dataset group name within the file stored."""
        return self.base.attributes.get("dataset_name")

    @property
    def file_path(self):
        """Return the absolute path the file stored."""
        return self.get_remote_path()
