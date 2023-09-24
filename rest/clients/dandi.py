from dandi.dandiapi import DandiAPIClient
from dandischema.models import Dandiset
import concurrent.futures


class DandiClient:

    def __init__(self):
        self.dandi_client = DandiAPIClient()

    def get_dandiset_metadata(self, dandiset_id: str, version_id: str = "draft"):
        dandiset = self.dandi_client.get_dandiset(dandiset_id=dandiset_id, version_id=version_id)
        return dandiset.get_metadata()


    def list_dandiset_files(self, dandiset_id: str, version_id: str = "draft"):
        dandiset = self.dandi_client.get_dandiset(dandiset_id=dandiset_id, version_id=version_id)
        return [i.dict().get("path") for i in dandiset.get_assets() if i.dict().get("path").endswith(".nwb")]


    def get_file_url(self, dandiset_id: str, file_path: str, version_id: str = "draft"):
        asset = self.dandi_client.get_dandiset(dandiset_id=dandiset_id, version_id=version_id).get_asset_by_path(file_path)
        return asset.get_content_url(follow_redirects=1, strip_query=True)


    def has_nwb(self, metadata: Dandiset):
        if hasattr(metadata, "assetsSummary"):
            assets_summary = metadata.assetsSummary
            if hasattr(assets_summary, "dataStandard"):
                return any(x.identifier == "RRID:SCR_015242" for x in assets_summary.dataStandard)
        return False


    def process_dandiset(self, dandiset):
        try:
            metadata = dandiset.get_metadata()
            if self.has_nwb(metadata):
                return metadata
        except:
            pass
        return None


    def get_all_dandisets_metadata(self):
        all_metadata = []
        dandisets = list(self.dandi_client.get_dandisets())
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_dandiset, dandiset) for dandiset in dandisets]
            for future in concurrent.futures.as_completed(futures):
                metadata = future.result()
                if metadata:
                    all_metadata.append(metadata)
        return all_metadata


    def collect_relevant_metadata(self, metadata_list: list):
        """Extract only relevant text fields from metadata list"""
        all_metadata_formatted = []
        for m in metadata_list:
            try:
                title = m.name
                description = m.description
                if m.assetsSummary.approach:
                    approaches = [a.name for a in m.assetsSummary.approach]
                else:
                    approaches = []
                if m.assetsSummary.measurementTechnique:
                    measurement_techniques = [a.name for a in m.assetsSummary.measurementTechnique]
                else:
                    measurement_techniques = []
                if m.assetsSummary.variableMeasured:
                    variables_measured = [a for a in m.assetsSummary.variableMeasured]
                else:
                    variables_measured = []
                if m.assetsSummary.species:
                    species = [a.name for a in m.assetsSummary.species]
                else:
                    species = []
                all_metadata_formatted.append(
                    {
                        "dandiset_id": m.id,
                        "url": str(m.url),
                        "title": title,
                        "description": description,
                        "approaches": approaches,
                        "measurement_techniques": measurement_techniques,
                        "variables_measured": variables_measured,
                        "species": species,
                    }
                )
            except Exception as e:
                raise e
        return all_metadata_formatted
    
    
    def stringify_relevant_metadata(self, metadata_formatted: dict):
        """Convert metadata dict to string"""
        text = ""
        text += "Title: " + metadata_formatted["title"] + "\n"
        text += "Description: " + metadata_formatted["description"] + "\n"
        if "approaches" in metadata_formatted:
            text += "Approaches: " + ", ".join(metadata_formatted["approaches"]) + "\n"
        if "measurement_techniques" in metadata_formatted:
            text += "Measurement techniques: " + ", ".join(metadata_formatted["measurement_techniques"]) + "\n"
        if "variables_measured" in metadata_formatted:
            text += "Variables measured: " + ", ".join(metadata_formatted["variables_measured"]) + "\n"
        if "species" in metadata_formatted:
            text += "Species: " + ", ".join(metadata_formatted["species"]) + "\n"
        return text