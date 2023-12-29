using Microsoft.Extensions.Configuration;


Console.WriteLine("Running");

var configs = new ConfigurationBuilder()
                        .AddUserSecrets("pi azSpeech")
                        .Build();


Console.WriteLine($"Setting is {configs["test"]}");