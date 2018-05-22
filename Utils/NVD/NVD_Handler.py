import urllib2
import zipfile
import os
import json

if __name__ == "__main__":
    '''URL of nvd latest version'''
    url = "https://static.nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-modified.json.zip"

    '''setup file path and download NVD'''
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    '''Downloading..'''
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status)

    f.close()

    '''Unzip NVD file and delete zip file.'''
    zip_ref = zipfile.ZipFile(file_name, 'a')
    zip_ref.extractall(".\NVD_File\\Modified")
    zip_ref.close()

    os.remove(file_name)


def update_nvd_file(main_window):
    '''URL of nvd latest version'''
    url = "https://static.nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-modified.json.zip"

    '''setup file path and download NVD'''
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    main_window.print_to_log("NVD_Handler", "Downloading: %s Bytes: %s" % (file_name, file_size))

    '''Downloading..'''
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        main_window.print_to_log("NVD_Handler", status)

    f.close()

    '''Unzip NVD file and delete zip file.'''
    zip_ref = zipfile.ZipFile(file_name, 'a')
    zip_ref.extractall(".\NVD_File\\Modified")
    zip_ref.close()

    os.remove(file_name)
    main_window.print_to_log("NVD_Handler", "Done")

def get_vulnerability_db():
    """
    prints a string with NVD file.
    :return:
    """
    file_path = "Utils\\NVD\\NVD_File\\Modified\\nvdcve-1.0-modified.json"

    file_data = open(file_path)

    data = json.load(file_data)
    print json.dumps(data, indent=4, sort_keys=True)


def get_vulnerability_impact(list_of_apps, main_window):
    """
    Evaluate common vulnerabilities impact on sistem's confidentiality
    :param list_of_apps:
    :param main_window:
    :return: Damage score 0-10.
    """
    file_path = "Utils\\NVD\\NVD_File\\Modified\\nvdcve-1.0-modified.json"
    with open(file_path) as data_file:
        data = json.load(data_file)

    main_window.print_to_log("NVD_Handler", "Searching in NVD file...")

    NVD_score = 0.0

    for cve in data["CVE_Items"]:
        for vendor_data in cve["cve"]["affects"]["vendor"]["vendor_data"]:
            for product_data in vendor_data["product"]["product_data"]:
                if product_data["product_name"] in list_of_apps:
                    impact_score = cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
                    NVD_score += impact_score
                    main_window.print_to_log("NVD_Handler", "Found vulnerability!")
                    main_window.print_to_log("NVD_Handler",
                                                   "Impact score for " + product_data["product_name"] +
                                                   " is: " + str(impact_score))
                    main_window.print_to_log("NVD_Handler", "Description: "
                                             + cve["cve"]["description"]["description_data"][0]["value"])

    main_window.print_to_log("NVD_Handler", "System's apps weren't in the NVD! Good!!") if NVD_score==0 else None
    main_window.print_to_log("NVD_Handler", "Done")
    return 10 if NVD_score > 10 else NVD_score
