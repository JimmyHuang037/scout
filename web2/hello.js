// 实现接口的类
var HelloWorldGreeter = /** @class */ (function () {
    function HelloWorldGreeter(message) {
        this.message = message;
    }
    HelloWorldGreeter.prototype.greet = function () {
        var element = document.getElementById('greeting');
        if (element) {
            element.textContent = this.message;
            console.log("i'm jimmy!new ts");
        }
    };
    return HelloWorldGreeter;
}());
// 使用泛型的函数
function createGreeter(greeterType, message) {
    console.log("i'm jimmy!new ts");
    return new greeterType(message);
}
// 创建实例并使用
var greeter = createGreeter(HelloWorldGreeter, "Hello, World with TypeScript!");
greeter.greet();
