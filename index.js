
import genbankParser from './node_modules/genbank-parser/src/index.js';

const serverUrl = 'http://127.0.0.1:5000/show';
let content = null
document.getElementById('fileInput').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = function(event) {
            content = event.target.result;
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    console.log(this.responseText)
                    const cgv = new CGV.Viewer('#my-viewer', {
                        height: 800,
                        width: 800,
                    });
                    cgv.io.loadJSON(JSON.parse(this.responseText).data)
                    cgv.draw()
                }
            };
            xhttp.open("POST", serverUrl, true);
            xhttp.setRequestHeader('Content-Type', 'application/json');
            xhttp.setRequestHeader("Access-Control-Allow-Origin", "*")
            xhttp.send(JSON.stringify({"data": content}));
            
            return
            result = genbankParser(content);
            const size = result[0].size;
            console.log(`size: ${size}`);
            const features = result[0].features;
            const cgv = new CGV.Viewer('#my-viewer', {
                height: 800,
                width: 800,
                sequence: {
                    length: size
                }
            });
            for(let i = 0; i < features.length; i++){
                let feature = features[i];
                if (feature.type == "tRNA"){
                    let {start, end, strand, name} = feature
                    let notes = feature.notes;
                    cgv.addFeatures({
                        type: 'tRNA',
                        name: name + " " + notes.product[0],
                        start: start,
                        stop: end,
                        strand: strand,
                        source: 'genome-features',
                        legend: 'tRNA'
                    });
                } else if (feature.type == "promoter"){
                    let {start, end, strand, name} = feature
                    cgv.addFeatures({
                        type: 'promoter',
                        name: name,
                        start: start,
                        stop: end,
                        strand: strand,
                        source: 'genome-features',
                        legend: 'promoter'
                    });
                } else if (feature.type == "CDS"){
                    let {start, end, strand, name} = feature
                    let notes = feature.notes;
                    cgv.addFeatures({
                        type: 'CDS',
                        name: name + " " + notes.product[0],
                        start: start,
                        stop: end,
                        strand: strand,
                        source: 'genome-features',
                        legend: 'CDS'
                    });
                }
            }
            var legendItem = cgv.legend.items();
            legendItem[0].color = 'green';
            legendItem[0].decoration = 'arrow';
            legendItem[1].color = 'blue';
            legendItem[1].decoration = 'arrow';
            legendItem[2].color = 'orange';
            legendItem[2].decoration = 'arrow';
            cgv.addTracks({
                name: 'Feature Track',
                separateFeaturesBy: 'strand',
                position: 'both',
                dataType: 'feature',
                dataMethod: 'source',
                dataKeys: 'genome-features'
            });
            cgv.draw();
            document.getElementById('fileInput').value = null;
        };
    } else {
        document.getElementById('fileContent').textContent = 'No file selected';
    }
});


// document.getElementById('searchButton').addEventListener('click', function() {
//     const name = document.getElementById('nameInput').value;
//     let outputText = "";
//     console.log(name)
//     if((name != "") && (result != null)){
//         const features = content.result[0].features;
//         for(let i = 0; i < features.length; i++){
//             let feature = features[i];
//             if (feature.name == name){
//                 let {type, start, end, strand, name} = feature
//                 let notes = feature.notes;
//                 let proteinId = notes.protein_id == null ? "" : notes.protein_id
//                 outputText += `${type} ${name}${notes.product ? " " + notes.product[0]:""}: 
//                     ${proteinId?`protein id=${proteinId}, `:""}${notes.note?`note=${notes.note}, `:""}
//                     strand=${strand}, ${start}:${end}<br>`;
//                 if (notes.translation){
//                     const translation = notes.translation[0];
//                     let l = translation.length;
//                     for (let i = 0; i < l; i += 50){
//                         outputText += `${translation.slice(i, Math.min(i+50, l))}<br>`
//                     }
                    
//                 }
//             }
//         }
//         document.getElementById('output').innerHTML = outputText;
//     }
//     document.getElementById('nameInput').value = "";
// });
