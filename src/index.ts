import * as AWS from "aws-sdk";

export const handler = async (): Promise<void> => {
    // なんらかの集計処理・・・
    const result = {
        sample_id: Date.now()
    }
    console.log(result);
};