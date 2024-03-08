// See https://aka.ms/new-console-template for more information
using System.Diagnostics;



var client = new HttpClient
{
    BaseAddress = new(args[0])
};


await using var stream = CaptureAudioStream();

await SendStreamToApiAsync(stream);

//ListAudioDevices();



static void ListAudioDevices()
{
    ProcessStartInfo psi = new ProcessStartInfo
    {
        FileName = "arecord",
        Arguments = "-l", // Lists the recording sound devices
        UseShellExecute = false,
        RedirectStandardOutput = true,
        CreateNoWindow = true
    };

    try
    {
        using (Process process = Process.Start(psi))
        {
            using (System.IO.StreamReader reader = process.StandardOutput)
            {
                string result = reader.ReadToEnd();
                Console.Write(result);
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"An error occurred: {ex.Message}");
    }
}


Stream CaptureAudioStream()
{
    var psi = new ProcessStartInfo
    {
        FileName = "arecord",
        Arguments = $"-D plughw:1,0 -f S16_LE -t wav -r 16000 -c 1 -",
        UseShellExecute = false,
        RedirectStandardOutput = true,
        CreateNoWindow = true
    };

    var process = new Process { StartInfo = psi };
    process.Start();
    return process.StandardOutput.BaseStream;
}



async Task SendStreamToApiAsync(Stream incoming)
{
    await using var outgoing = new MemoryStream();
    var request = new HttpRequestMessage(HttpMethod.Post, "audioToSpecificFile")
    {
        Content = new StreamContent(outgoing)
    };
    await Console.Out.WriteLineAsync("Copying stream...");
    await incoming.CopyToAsync(outgoing);
    await Console.Out.WriteLineAsync("Sending Stream");
    await client.SendAsync(request);
    await Console.Out.WriteLineAsync("Request sent");
}