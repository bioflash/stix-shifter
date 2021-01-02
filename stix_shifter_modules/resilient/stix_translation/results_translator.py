from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import json_to_stix_translator
from os import path
import json
import ipaddress


class ResultsTranslator(BaseResultTranslator):

    def translate_results(self, data_source, data):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :return: STIX formatted results
        :rtype: str
        """

        json_data = json.loads(data)['data']
        data_source = json.loads(data_source)

        results = json_to_stix_translator.convert_to_stix(data_source, self.map_data,
                                                          map(self.transformRecords, json_data), self.transformers,
                                                          self.options)

        if len(results['objects']) - 1 == len(json_data):
            for i in range(1, len(results['objects'])):
                results['objects'][i]['number_observed'] = 1
        else:
            raise RuntimeError("Incorrect number of result objects after translation. Found: {}, expected: {}.".format(
                len(results['objects']) - 1, len(json_data)))

        return results

    def transformRecords(self, record):
        value = record['value']

        result = {"RelatedCaseCount": record['related_incident_count'],
                  "LastRelatedCase": record['last_related_inc_id'],
                  "FirstRelatedCase": record['first_related_inc_id']}
        if record['type'] == 2:
            result['DomainName'] = value
        elif record['type'] == 1:
            try:
                ipaddress.IPv6Address(value)
                result["IPV6Addr"] = value
            except:
                result["IPV4Addr"] = value

        return  result