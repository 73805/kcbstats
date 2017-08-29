import { Pipe, PipeTransform } 	from '@angular/core';

// map to flag position in square
@Pipe({name: 'flagPos'})
export class FlagPosPipe implements PipeTransform {
	transform(abbrev) : string {
		let flag_lookup: object = {"ak": "right","al": "center","ar": "center","az": "center","ca": "center","co": "left","ct": "center","de": "center","fl": "center","ga": "left","hi": "left","ia": "center","id": "center","il": "center","in": "center","ks": "center","ky": "center","la": "center","ma": "center","md": "center","me": "center","mi": "right","mn": "center","mo": "center","ms": "left","mt": "center","nc": "left","nd": "center","ne": "center","nh": "center","nj": "center","nm": "center","nv": "left","ny": "center","oh": "left","ok": "center","or": "center","pa": "center","ri": "center","sc": "center","sd": "center","tn": "center","tx": "left","ut": "center","va": "center","vt": "center","wa": "center","wi": "center","wv": "center","wy": "center"};
		if(flag_lookup.hasOwnProperty(abbrev)){
			return flag_lookup[abbrev];
		}else{
			return "center";
			
		}
	}
}