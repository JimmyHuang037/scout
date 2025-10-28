// 定义一个接口
interface Greeter {
    message: string;
    greet(): void;
}

// 实现接口的类
class HelloWorldGreeter implements Greeter {
    message: string;

    constructor(message: string) {
        this.message = message;
    }

    greet(): void {
        const element = document.getElementById('greeting');
        if (element) {
            element.textContent = this.message;
            console.log("i'm jimmy!new ts");
        }
    }
}

// 使用泛型的函数
function createGreeter<T extends Greeter>(greeterType: new (message: string) => T, message: string): T {
    console.log("i'm jimmy!new ts");
    return new greeterType(message);
}

// 创建实例并使用
const greeter = createGreeter(HelloWorldGreeter, "Hello, World with TypeScript!");
greeter.greet();