
using Microsoft.Extensions.Configuration;

var configs = new ConfigurationBuilder()
                        .AddUserSecrets("pi azSpeech")
                        .Build();


Console.WriteLine($"Setting is {configs["test"]}");