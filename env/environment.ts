import { load } from "js-yaml";
import { readFileSync } from "fs";

export class Environment {
    region: string;
    id: number;
    
    constructor(env: provisioned){
        const config = load(readFileSync('env\\env.yaml', "utf8")) as Config;
        this.region = config[env].region;
        this.id = config[env].id;
    }
}
type provisioned = 'dev' | 'stg' | 'prd';
type Config = {
    dev: {
        region: string;
        id: number;
    },
    stg: {
        region: string;
        id: number;
    },
    prd: {
        region: string;
        id: number;
    }
}

// const env = new environment('dev');
// console.log(env.id);