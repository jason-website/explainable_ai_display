pipeline {
  agent any
  triggers {
    GenericTrigger(
            genericVariables: [
                    [key: 'commit', value: '$.commits[0].id'],
                    [key: 'committer', value: '$.commits[0].committer.name'],
                    [key: 'ref', value: '$.ref']
            ],
            token: 'explainable_ai_display',
            causeString: 'Triggered by github webhook on commit $commit to $ref by $committer',
            printContributedVariables: true,
            printPostContent: true,
            silentResponse: true
    )
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('DOCKERHUB_USR')
  }

  stages {
    stage('Checkout') {
      steps {
  checkout([$class: 'GitSCM', branches: [[name: '*/master']],
         doGenerateSubmoduleConfigurations: false,
         extensions: [],
         submoduleCfg: [],
         userRemoteConfigs: [[url: 'https://github.com/jason-website/explainable_ai_display.git']]])

      }
    }

    stage('Generate The Image') {
      steps {
        echo "generate the image"
        sh '''
         set +x
          chmod +x ./ci/gen-image.sh
          ./ci/gen-image.sh
         '''
        }
    }

    stage('Push Image To Docker hub') {
      steps {
        echo "push image to docker hub"
        sh '''
         set +x
         chmod +x ./ci/push-image.sh
         ./ci/push-image.sh
         '''
      }
    }

    stage('Deploy') {
              options {
                  timeout(time: 60, unit: 'SECONDS')
              }

              input {
                  message 'Do you want to deploy?'
                  ok 'Yes, go ahead.'
              }

              steps {
                  sh '''
                  set +x
                  ./ci/deploy.sh
                  '''
              }
            }
  }
}
