'''
Created on 12 Jan 2017
@author: xuepeng
'''

import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root,dirs, files in os.walk(path):
        for f in files:
            ziph.write(os.path.join("dependency-files/", f))
            
def zipFileWithTargetPath(jsonStr,output):     
    message = """   
    <html>
        <head>
            <meta http-equiv="Content_Type" content="text/html; charset=UTF-8" />
            <link type="text/css" rel="stylesheet" href="./dependency-files/style.css" />
            <link type="text/css" rel="stylesheet" href="./dependency-files/bootstrap.min.css" />
            <script type="text/javascript" src="./dependency-files/d3.layout.js"></script>
            <script type="text/javascript" src="./dependency-files/d3pie.js"></script>
            <script type="text/javascript" src="./dependency-files/jquery.js"></script>
            <script type="text/javascript" src="./dependency-files/d3.min.js"></script>
        </head>
        <body>
            <div id="header">Offline Web-based Interactive Clustering Analysis Report</div>
            <div id="body"></div>
            <div id="popup">
                <div class="row">
                    <div class="col-md-4" id="pie_gender"></div>
                    <div class="col-md-4" id="pie_age"></div>
                    <div class="col-md-4" id="pie_freq"></div>
                </div>
            </div>
            <script type="text/javascript">var flare = '"""+ jsonStr +"""' </script>
            <script type="text/javascript" src="./dependency-files/clusterReport.js"></script>
        </body>
    </html>
    """
    if os.path.exists(output + '/zipfile_writestr.zip'):
        os.remove(output + '/zipfile_writestr.zip')
        
    
    
    zf = zipfile.ZipFile(output + '/zipfile_writestr.zip', 
                     mode='a',
                     compression=zipfile.ZIP_DEFLATED, 
                     )
    try:        
        zf.writestr('offline_clustering_report.html', message)
        zipdir("dependency-files/", zf)
    finally:
        zf.close()   

            
def zipFile(jsonStr):     
    message = """   
    <html>
        <head>
            <meta http-equiv="Content_Type" content="text/html; charset=UTF-8" />
            <link type="text/css" rel="stylesheet" href="./dependency-files/style.css" />
            <link type="text/css" rel="stylesheet" href="./dependency-files/bootstrap.min.css" />
            <script type="text/javascript" src="./dependency-files/d3.layout.js.download"></script>
            <script type="text/javascript" src="./dependency-files/d3pie.js"></script>
            <script type="text/javascript" src="./dependency-files/jquery.js"></script>
            <script type="text/javascript" src="./dependency-files/d3.min.js"></script>
        </head>
        <body>
            <div id="header">Offline Web-based Interactive Clustering Analysis Report</div>
            <div id="body"></div>
            <div id="popup">
                <div class="row">
                    <div class="col-md-4" id="pie_gender"></div>
                    <div class="col-md-4" id="pie_age"></div>
                    <div class="col-md-4" id="pie_freq"></div>
                </div>
            </div>
            <script type="text/javascript">var flare = '"""+ jsonStr +"""' </script>
            <script type="text/javascript" src="./dependency-files/clusterReport.js"></script>
        </body>
    </html>
    """
    if os.path.exists('zipfile_writestr.zip'):
        os.remove('zipfile_writestr.zip')
    
    zf = zipfile.ZipFile('zipfile_writestr.zip', 
                     mode='a',
                     compression=zipfile.ZIP_DEFLATED, 
                     )
           
    try:        
        zf.writestr('offline_clustering_report.html', message)
        zipdir('dependency-files', zf)
    finally:
        zf.close()       
            

if __name__ == '__main__':
    
    value = "{\"name\":1000,\"clusterId\": \"Initial Data\",\"eth\":{\"e200035\":25,\"e200014\":1,\"e200003\":1,\"e200038\":1,\"e200005\":41,\"e200017\":1,\"e200039\":1,\"e200006\":1,\"e200018\":82,\"e200008\":1,\"e200080\":150,\"e200083\":652,\"e200063\":28,\"e200042\":2,\"e200064\":8,\"e200087\":2,\"e200043\":1,\"e200077\":1,\"e200056\":1},\"payor\":{\"p200035\":25,\"p200014\":1,\"p200003\":1,\"p200038\":1,\"p200005\":41,\"p200017\":1,\"p200039\":1,\"p200006\":1,\"p200018\":82,\"p200008\":1,\"p200080\":150,\"p200083\":652,\"p200063\":28,\"p200042\":2,\"p200064\":8,\"p200087\":2,\"p200043\":1,\"p200077\":1,\"p200056\":1},\"adm\":{\"a200035\":25,\"a200014\":1,\"a200003\":1,\"a200038\":1,\"a200005\":41,\"a200017\":1,\"a200039\":1,\"a200006\":1,\"a200018\":82,\"a200008\":1,\"a200080\":150,\"a200083\":652,\"a200063\":28,\"a200042\":2,\"a200064\":8,\"a200087\":2,\"a200043\":1,\"a200077\":1,\"a200056\":1},\"children\":[{\"name\":197,\"clusterId\":0,\"eth\":{\"e200035\":5,\"e200005\":4,\"e200006\":1,\"e200018\":13,\"e200080\":32,\"e200083\":134,\"e200063\":5,\"e200064\":2,\"e200087\":1},\"payor\":{\"p200035\":5,\"p200005\":4,\"p200006\":1,\"p200018\":13,\"p200080\":32,\"p200083\":134,\"p200063\":5,\"p200064\":2,\"p200087\":1},\"adm\":{\"a200035\":5,\"a200005\":4,\"a200006\":1,\"a200018\":13,\"a200080\":32,\"a200083\":134,\"a200063\":5,\"a200064\":2,\"a200087\":1},\"children\":[{\"name\":46,\"clusterId\":0,\"eth\":{\"e200035\":2,\"e200018\":4,\"e200080\":9,\"e200083\":27,\"e200063\":2,\"e200064\":2},\"payor\":{\"p200035\":2,\"p200018\":4,\"p200080\":9,\"p200083\":27,\"p200063\":2,\"p200064\":2},\"adm\":{\"a200035\":2,\"a200018\":4,\"a200080\":9,\"a200083\":27,\"a200063\":2,\"a200064\":2},\"size\":541},{\"name\":40,\"clusterId\":1,\"eth\":{\"e200035\":2,\"e200005\":1,\"e200018\":2,\"e200080\":6,\"e200083\":28,\"e200063\":1},\"payor\":{\"p200035\":2,\"p200005\":1,\"p200018\":2,\"p200080\":6,\"p200083\":28,\"p200063\":1},\"adm\":{\"a200035\":2,\"a200005\":1,\"a200018\":2,\"a200080\":6,\"a200083\":28,\"a200063\":1},\"size\":576},{\"name\":23,\"clusterId\":2,\"eth\":{\"e200018\":2,\"e200080\":3,\"e200083\":18},\"payor\":{\"p200018\":2,\"p200080\":3,\"p200083\":18},\"adm\":{\"a200018\":2,\"a200080\":3,\"a200083\":18},\"size\":851},{\"name\":58,\"clusterId\":3,\"eth\":{\"e200035\":1,\"e200005\":3,\"e200006\":1,\"e200018\":3,\"e200080\":9,\"e200083\":39,\"e200063\":1,\"e200087\":1},\"payor\":{\"p200035\":1,\"p200005\":3,\"p200006\":1,\"p200018\":3,\"p200080\":9,\"p200083\":39,\"p200063\":1,\"p200087\":1},\"adm\":{\"a200035\":1,\"a200005\":3,\"a200006\":1,\"a200018\":3,\"a200080\":9,\"a200083\":39,\"a200063\":1,\"a200087\":1},\"size\":976},{\"name\":30,\"clusterId\":4,\"eth\":{\"e200018\":2,\"e200080\":5,\"e200083\":22,\"e200063\":1},\"payor\":{\"p200018\":2,\"p200080\":5,\"p200083\":22,\"p200063\":1},\"adm\":{\"a200018\":2,\"a200080\":5,\"a200083\":22,\"a200063\":1},\"size\":719}]},{\"name\":87,\"clusterId\":1,\"eth\":{\"e200035\":3,\"e200005\":3,\"e200018\":7,\"e200080\":12,\"e200083\":58,\"e200063\":2,\"e200064\":1,\"e200077\":1},\"payor\":{\"p200035\":3,\"p200005\":3,\"p200018\":7,\"p200080\":12,\"p200083\":58,\"p200063\":2,\"p200064\":1,\"p200077\":1},\"adm\":{\"a200035\":3,\"a200005\":3,\"a200018\":7,\"a200080\":12,\"a200083\":58,\"a200063\":2,\"a200064\":1,\"a200077\":1},\"size\":810},{\"name\":659,\"clusterId\":2,\"eth\":{\"e200035\":17,\"e200014\":1,\"e200003\":1,\"e200038\":1,\"e200005\":33,\"e200017\":1,\"e200039\":1,\"e200018\":54,\"e200008\":1,\"e200080\":99,\"e200083\":421,\"e200063\":19,\"e200042\":2,\"e200064\":5,\"e200087\":1,\"e200043\":1,\"e200056\":1},\"payor\":{\"p200035\":17,\"p200014\":1,\"p200003\":1,\"p200038\":1,\"p200005\":33,\"p200017\":1,\"p200039\":1,\"p200018\":54,\"p200008\":1,\"p200080\":99,\"p200083\":421,\"p200063\":19,\"p200042\":2,\"p200064\":5,\"p200087\":1,\"p200043\":1,\"p200056\":1},\"adm\":{\"a200035\":17,\"a200014\":1,\"a200003\":1,\"a200038\":1,\"a200005\":33,\"a200017\":1,\"a200039\":1,\"a200018\":54,\"a200008\":1,\"a200080\":99,\"a200083\":421,\"a200063\":19,\"a200042\":2,\"a200064\":5,\"a200087\":1,\"a200043\":1,\"a200056\":1},\"children\":[{\"name\":136,\"clusterId\":0,\"eth\":{\"e200035\":3,\"e200003\":1,\"e200038\":1,\"e200005\":1,\"e200039\":1,\"e200018\":11,\"e200080\":29,\"e200083\":84,\"e200063\":2,\"e200064\":2,\"e200087\":1},\"payor\":{\"p200035\":3,\"p200003\":1,\"p200038\":1,\"p200005\":1,\"p200039\":1,\"p200018\":11,\"p200080\":29,\"p200083\":84,\"p200063\":2,\"p200064\":2,\"p200087\":1},\"adm\":{\"a200035\":3,\"a200003\":1,\"a200038\":1,\"a200005\":1,\"a200039\":1,\"a200018\":11,\"a200080\":29,\"a200083\":84,\"a200063\":2,\"a200064\":2,\"a200087\":1},\"children\":[{\"name\":44,\"clusterId\":0,\"eth\":{\"e200038\":1,\"e200039\":1,\"e200083\":42},\"payor\":{\"p200038\":1,\"p200039\":1,\"p200083\":42},\"adm\":{\"a200038\":1,\"a200039\":1,\"a200083\":42},\"size\":804},{\"name\":29,\"clusterId\":1,\"eth\":{\"e200035\":2,\"e200018\":2,\"e200080\":5,\"e200083\":19,\"e200063\":1},\"payor\":{\"p200035\":2,\"p200018\":2,\"p200080\":5,\"p200083\":19,\"p200063\":1},\"adm\":{\"a200035\":2,\"a200018\":2,\"a200080\":5,\"a200083\":19,\"a200063\":1},\"size\":879},{\"name\":17,\"clusterId\":2,\"eth\":{\"e200018\":1,\"e200080\":14,\"e200063\":1,\"e200064\":1},\"payor\":{\"p200018\":1,\"p200080\":14,\"p200063\":1,\"p200064\":1},\"adm\":{\"a200018\":1,\"a200080\":14,\"a200063\":1,\"a200064\":1},\"size\":902},{\"name\":24,\"clusterId\":3,\"eth\":{\"e200035\":1,\"e200003\":1,\"e200005\":1,\"e200018\":5,\"e200080\":7,\"e200083\":8,\"e200087\":1},\"payor\":{\"p200035\":1,\"p200003\":1,\"p200005\":1,\"p200018\":5,\"p200080\":7,\"p200083\":8,\"p200087\":1},\"adm\":{\"a200035\":1,\"a200003\":1,\"a200005\":1,\"a200018\":5,\"a200080\":7,\"a200083\":8,\"a200087\":1},\"size\":623},{\"name\":22,\"clusterId\":4,\"eth\":{\"e200018\":3,\"e200080\":3,\"e200083\":15,\"e200064\":1},\"payor\":{\"p200018\":3,\"p200080\":3,\"p200083\":15,\"p200064\":1},\"adm\":{\"a200018\":3,\"a200080\":3,\"a200083\":15,\"a200064\":1},\"size\":849}]},{\"name\":155,\"clusterId\":1,\"eth\":{\"e200035\":4,\"e200005\":17,\"e200018\":13,\"e200008\":1,\"e200080\":12,\"e200083\":102,\"e200063\":6},\"payor\":{\"p200035\":4,\"p200005\":17,\"p200018\":13,\"p200008\":1,\"p200080\":12,\"p200083\":102,\"p200063\":6},\"adm\":{\"a200035\":4,\"a200005\":17,\"a200018\":13,\"a200008\":1,\"a200080\":12,\"a200083\":102,\"a200063\":6},\"children\":[{\"name\":62,\"clusterId\":0,\"eth\":{\"e200035\":2,\"e200005\":10,\"e200083\":45,\"e200063\":5},\"payor\":{\"p200035\":2,\"p200005\":10,\"p200083\":45,\"p200063\":5},\"adm\":{\"a200035\":2,\"a200005\":10,\"a200083\":45,\"a200063\":5},\"size\":938},{\"name\":25,\"clusterId\":1,\"eth\":{\"e200005\":1,\"e200018\":1,\"e200080\":3,\"e200083\":19,\"e200063\":1},\"payor\":{\"p200005\":1,\"p200018\":1,\"p200080\":3,\"p200083\":19,\"p200063\":1},\"adm\":{\"a200005\":1,\"a200018\":1,\"a200080\":3,\"a200083\":19,\"a200063\":1},\"size\":712},{\"name\":46,\"clusterId\":2,\"eth\":{\"e200035\":1,\"e200018\":4,\"e200080\":5,\"e200083\":36},\"payor\":{\"p200035\":1,\"p200018\":4,\"p200080\":5,\"p200083\":36},\"adm\":{\"a200035\":1,\"a200018\":4,\"a200080\":5,\"a200083\":36},\"size\":848},{\"name\":14,\"clusterId\":3,\"eth\":{\"e200035\":1,\"e200005\":6,\"e200018\":1,\"e200008\":1,\"e200080\":3,\"e200083\":2},\"payor\":{\"p200035\":1,\"p200005\":6,\"p200018\":1,\"p200008\":1,\"p200080\":3,\"p200083\":2},\"adm\":{\"a200035\":1,\"a200005\":6,\"a200018\":1,\"a200008\":1,\"a200080\":3,\"a200083\":2},\"size\":789},{\"name\":8,\"clusterId\":4,\"eth\":{\"e200018\":7,\"e200080\":1},\"payor\":{\"p200018\":7,\"p200080\":1},\"adm\":{\"a200018\":7,\"a200080\":1},\"size\":938}]},{\"name\":143,\"clusterId\":2,\"eth\":{\"e200035\":4,\"e200005\":7,\"e200018\":11,\"e200080\":17,\"e200083\":95,\"e200063\":6,\"e200042\":1,\"e200064\":2},\"payor\":{\"p200035\":4,\"p200005\":7,\"p200018\":11,\"p200080\":17,\"p200083\":95,\"p200063\":6,\"p200042\":1,\"p200064\":2},\"adm\":{\"a200035\":4,\"a200005\":7,\"a200018\":11,\"a200080\":17,\"a200083\":95,\"a200063\":6,\"a200042\":1,\"a200064\":2},\"children\":[{\"name\":24,\"clusterId\":0,\"eth\":{\"e200035\":2,\"e200005\":1,\"e200018\":3,\"e200080\":4,\"e200083\":12,\"e200063\":1,\"e200064\":1},\"payor\":{\"p200035\":2,\"p200005\":1,\"p200018\":3,\"p200080\":4,\"p200083\":12,\"p200063\":1,\"p200064\":1},\"adm\":{\"a200035\":2,\"a200005\":1,\"a200018\":3,\"a200080\":4,\"a200083\":12,\"a200063\":1,\"a200064\":1},\"size\":735},{\"name\":44,\"clusterId\":1,\"eth\":{\"e200035\":1,\"e200005\":5,\"e200018\":5,\"e200080\":1,\"e200083\":29,\"e200063\":2,\"e200064\":1},\"payor\":{\"p200035\":1,\"p200005\":5,\"p200018\":5,\"p200080\":1,\"p200083\":29,\"p200063\":2,\"p200064\":1},\"adm\":{\"a200035\":1,\"a200005\":5,\"a200018\":5,\"a200080\":1,\"a200083\":29,\"a200063\":2,\"a200064\":1},\"size\":577},{\"name\":30,\"clusterId\":2,\"eth\":{\"e200035\":1,\"e200005\":1,\"e200080\":8,\"e200083\":18,\"e200063\":1,\"e200042\":1},\"payor\":{\"p200035\":1,\"p200005\":1,\"p200080\":8,\"p200083\":18,\"p200063\":1,\"p200042\":1},\"adm\":{\"a200035\":1,\"a200005\":1,\"a200080\":8,\"a200083\":18,\"a200063\":1,\"a200042\":1},\"size\":936},{\"name\":15,\"clusterId\":3,\"eth\":{\"e200018\":2,\"e200083\":11,\"e200063\":2},\"payor\":{\"p200018\":2,\"p200083\":11,\"p200063\":2},\"adm\":{\"a200018\":2,\"a200083\":11,\"a200063\":2},\"size\":902},{\"name\":30,\"clusterId\":4,\"eth\":{\"e200018\":1,\"e200080\":4,\"e200083\":25},\"payor\":{\"p200018\":1,\"p200080\":4,\"p200083\":25},\"adm\":{\"a200018\":1,\"a200080\":4,\"a200083\":25},\"size\":728}]},{\"name\":106,\"clusterId\":3,\"eth\":{\"e200035\":5,\"e200014\":1,\"e200005\":6,\"e200018\":9,\"e200080\":19,\"e200083\":61,\"e200063\":3,\"e200064\":1,\"e200056\":1},\"payor\":{\"p200035\":5,\"p200014\":1,\"p200005\":6,\"p200018\":9,\"p200080\":19,\"p200083\":61,\"p200063\":3,\"p200064\":1,\"p200056\":1},\"adm\":{\"a200035\":5,\"a200014\":1,\"a200005\":6,\"a200018\":9,\"a200080\":19,\"a200083\":61,\"a200063\":3,\"a200064\":1,\"a200056\":1},\"children\":[{\"name\":36,\"clusterId\":0,\"eth\":{\"e200005\":1,\"e200083\":34,\"e200063\":1},\"payor\":{\"p200005\":1,\"p200083\":34,\"p200063\":1},\"adm\":{\"a200005\":1,\"a200083\":34,\"a200063\":1},\"size\":551},{\"name\":25,\"clusterId\":1,\"eth\":{\"e200035\":4,\"e200014\":1,\"e200005\":3,\"e200080\":13,\"e200083\":1,\"e200063\":2,\"e200064\":1},\"payor\":{\"p200035\":4,\"p200014\":1,\"p200005\":3,\"p200080\":13,\"p200083\":1,\"p200063\":2,\"p200064\":1},\"adm\":{\"a200035\":4,\"a200014\":1,\"a200005\":3,\"a200080\":13,\"a200083\":1,\"a200063\":2,\"a200064\":1},\"size\":522},{\"name\":28,\"clusterId\":2,\"eth\":{\"e200035\":1,\"e200005\":2,\"e200018\":1,\"e200080\":4,\"e200083\":20},\"payor\":{\"p200035\":1,\"p200005\":2,\"p200018\":1,\"p200080\":4,\"p200083\":20},\"adm\":{\"a200035\":1,\"a200005\":2,\"a200018\":1,\"a200080\":4,\"a200083\":20},\"size\":775},{\"name\":11,\"clusterId\":3,\"eth\":{\"e200018\":2,\"e200080\":2,\"e200083\":6,\"e200056\":1},\"payor\":{\"p200018\":2,\"p200080\":2,\"p200083\":6,\"p200056\":1},\"adm\":{\"a200018\":2,\"a200080\":2,\"a200083\":6,\"a200056\":1},\"size\":691},{\"name\":6,\"clusterId\":4,\"eth\":{\"e200018\":6},\"payor\":{\"p200018\":6},\"adm\":{\"a200018\":6},\"size\":737}]},{\"name\":119,\"clusterId\":4,\"eth\":{\"e200035\":1,\"e200005\":2,\"e200017\":1,\"e200018\":10,\"e200080\":22,\"e200083\":79,\"e200063\":2,\"e200042\":1,\"e200043\":1},\"payor\":{\"p200035\":1,\"p200005\":2,\"p200017\":1,\"p200018\":10,\"p200080\":22,\"p200083\":79,\"p200063\":2,\"p200042\":1,\"p200043\":1},\"adm\":{\"a200035\":1,\"a200005\":2,\"a200017\":1,\"a200018\":10,\"a200080\":22,\"a200083\":79,\"a200063\":2,\"a200042\":1,\"a200043\":1},\"children\":[{\"name\":5,\"clusterId\":0,\"eth\":{\"e200005\":1,\"e200018\":3,\"e200080\":1},\"payor\":{\"p200005\":1,\"p200018\":3,\"p200080\":1},\"adm\":{\"a200005\":1,\"a200018\":3,\"a200080\":1},\"size\":736},{\"name\":23,\"clusterId\":1,\"eth\":{\"e200035\":1,\"e200017\":1,\"e200018\":5,\"e200080\":14,\"e200042\":1,\"e200043\":1},\"payor\":{\"p200035\":1,\"p200017\":1,\"p200018\":5,\"p200080\":14,\"p200042\":1,\"p200043\":1},\"adm\":{\"a200035\":1,\"a200017\":1,\"a200018\":5,\"a200080\":14,\"a200042\":1,\"a200043\":1},\"size\":957},{\"name\":15,\"clusterId\":2,\"eth\":{\"e200080\":5,\"e200083\":9,\"e200063\":1},\"payor\":{\"p200080\":5,\"p200083\":9,\"p200063\":1},\"adm\":{\"a200080\":5,\"a200083\":9,\"a200063\":1},\"size\":522},{\"name\":58,\"clusterId\":3,\"eth\":{\"e200083\":57,\"e200063\":1},\"payor\":{\"p200083\":57,\"p200063\":1},\"adm\":{\"a200083\":57,\"a200063\":1},\"size\":984},{\"name\":18,\"clusterId\":4,\"eth\":{\"e200005\":1,\"e200018\":2,\"e200080\":2,\"e200083\":13},\"payor\":{\"p200005\":1,\"p200018\":2,\"p200080\":2,\"p200083\":13},\"adm\":{\"a200005\":1,\"a200018\":2,\"a200080\":2,\"a200083\":13},\"size\":788}]}]},{\"name\":15,\"clusterId\":3,\"eth\":{\"e200018\":3,\"e200080\":2,\"e200083\":9,\"e200063\":1},\"payor\":{\"p200018\":3,\"p200080\":2,\"p200083\":9,\"p200063\":1},\"adm\":{\"a200018\":3,\"a200080\":2,\"a200083\":9,\"a200063\":1},\"size\":872},{\"name\":42,\"clusterId\":4,\"eth\":{\"e200005\":1,\"e200018\":5,\"e200080\":5,\"e200083\":30,\"e200063\":1},\"payor\":{\"p200005\":1,\"p200018\":5,\"p200080\":5,\"p200083\":30,\"p200063\":1},\"adm\":{\"a200005\":1,\"a200018\":5,\"a200080\":5,\"a200083\":30,\"a200063\":1},\"size\":692}]}"
    zipFile(value) 
    

#
    