
// generate random string, length === len
export function randomString(len) {
    len = len || 32;
    let t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",
        a = t.length,
        n = "";
    for(let i = 0; i < len; i++) n += t.charAt(Math.floor(Math.random() * a));
    return n;
}