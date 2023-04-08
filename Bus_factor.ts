import { Octokit } from "@octokit/rest";

const octokit = new Octokit({
    auth: "your_github_access_token"
  });
  

  
  // Function to calculate bus factor score
  async function calculateBusFactor(owner: string, repo: string) {
    // Get the list of contributors
    const contributors = await octokit.repos.listContributors({
      owner,
      repo
    });
  
    // Calculate the total number of lines of code committed by all contributors
    const totalLinesOfCode = contributors.data.reduce((acc, c) => {
      // Accumulate the total number of lines of code by adding the contributions of each contributor
      return acc + c.contributions;
    }, 0);
  
    // Calculate the number of unique contributors
    const uniqueContributors = new Set(contributors.data.map(c => c.login));
  
    // Return the bus factor score
    return uniqueContributors.size / totalLinesOfCode;
  }
  
  const owner = "owner";
  const repo = "repo";
  
  // Call the calculateBusFactor function and log the result
  calculateBusFactor(owner, repo).then(busFactor => {
    console.log(`The bus factor score is: ${busFactor}`);
  });
  
  
 
  