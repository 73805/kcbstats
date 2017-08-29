import { Injectable }               from '@angular/core';

@Injectable()
export class DetailService {

	// sort an array of object by a property
	sortOnKey(ar, prop, ascending){
		if(ascending){
			return ar.sort(function(a, b){
				return parseFloat(a[prop]) - parseFloat(b[prop]);
			});
		}
		else{
			return ar.sort(function(a, b){
				return parseFloat(b[prop]) - parseFloat(a[prop]);
			});
		}
	}

	// convert an object of objects to an array of object with former keys as property key
	// then sort the array of objects on a property
	sortTransformObj(obj, prop, ascending){
		let ar = [];
		for(let okey in obj){
			if(obj.hasOwnProperty(okey)){
			    let subObj = obj[okey];
			    subObj.key = okey;
			    ar.push(subObj);
			}
		}
		return this.sortOnKey(ar, prop, ascending);
	}

	// construct an object of arrays (of objects) for waffle component digestion!
	constructScores(obj, date_order){
		let scores = {chicken: [], ribs: [], pork: [], brisket: []};
		let scores_keys = Object.keys(scores);
		let obj_keys = Object.keys(obj);
		// for each team
		for(let i = 0; i < obj_keys.length; i++){
			let okey = obj_keys[i]
			if(obj.hasOwnProperty(okey)){
				// for each category in the scores array
				for (let j = 0; j < scores_keys.length; j++){
					let ckey = scores_keys[j];
					if(obj[okey].hasOwnProperty(ckey)){
						if(date_order){
							scores[ckey].push({name: obj[okey].name, 
										score: obj[okey][ckey], 
										date_order: obj[okey].date_order});
						}
						else{
							scores[ckey].push({name: obj[okey].name, 
										 score: obj[okey][ckey]});
						}
					}
				}
			}
		};
		for (let j = 0; j < scores_keys.length; j++){
			let ckey = scores_keys[j];
			if(date_order){
				scores[ckey] = this.sortOnKey(scores[ckey], "date_order", true);
			}
			else{
				scores[ckey] = this.sortOnKey(scores[ckey], "score", false);
			}
		};
    		return scores;
	}
}