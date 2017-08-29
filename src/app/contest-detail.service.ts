import { Injectable }               from '@angular/core';
import { Observable, Subject }      from "rxjs/Rx";
import { AngularFireDatabase, 
         FirebaseListObservable, 
         FirebaseObjectObservable } from "angularfire2/database";

@Injectable()
export class ContestDetailService {
  
	constructor(private db: AngularFireDatabase) { }

	getContestDetails(contest_id: string): FirebaseObjectObservable<object> {
		return this.db.object("/contests/" + contest_id);
	}
}