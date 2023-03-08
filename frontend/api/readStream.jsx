// TODO: Share controller with fetch() to avoid hanging streams

export default function readStream(response) {
    const reader = response.body.getReader();
    const controller = new AbortController();
    const signal = controller.signal;

    // Create a new ReadableStream object and pipe the response body to it
    const stream = new ReadableStream({
      start(controller) {
        // Recursively push data to the stream
        function push() {
          reader.read().then(({ done, value }) => {
            if (done) {
              controller.close();
              return;
            }
            controller.enqueue(value);
            push();
          });
        }

        push();
      }
    });

    // Define the Symbol.asyncIterator method to make stream iterable
    stream[Symbol.asyncIterator] = () => {
        const reader = stream.getReader();
        return {
        async next() {
            const { done, value } = await reader.read();
            if (done) { return { done: true }; }
            return { done: false, value };
        },
        async return() {
            await reader.cancel();
            return { done: true };
        },
        };
    };

    return stream;
}