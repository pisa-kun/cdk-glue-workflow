import { load } from "js-yaml";
import { readFileSync } from "fs";

export class Environment {
    region: string;
    id: number;
    email: string;
    
    constructor(env: provisioned){
        const config = load(readFileSync('env\\env.yaml', "utf8")) as Config;
        this.region = config[env].region;
        this.id = config[env].id;
        this.email = config[env].email;
    }
}
type provisioned = 'dev' | 'stg' | 'prd';
type Config = {
    dev: {
        region: string;
        id: number;
        email: string;
    },
    stg: {
        region: string;
        id: number;
        email: string;
    },
    prd: {
        region: string;
        id: number;
        email: string;
    }
}

const env = new Environment('dev');
console.log(env.id, env.email);